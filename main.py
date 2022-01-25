import json
import os
import time
from requests import get, post
from decouple import config

# Loads and sets Home Assistant configurations
ha_token = config('HA_TOKEN')
ha_protocol = config('HA_PROTOCOL')
ha_host = config('HA_HOST')
ha_port = config('HA_PORT')

# Loads sleep delta
delta = config("DELTA")

# Loads entities
entities = config('ENTITIES').split(';')

# Creates folder structure
sensor_data = "sensor_data"
if not os.path.exists(sensor_data):
    os.makedirs(sensor_data)

# Keeps application up and running
while True:

    # Loops through entities
    for entity in entities:

        # entity_id,unit
        entity_id = entity.split(',')[0]
        friendly_name = entity.split(',')[1]

        # Gets current Wattage from sensor from Home Assistant
        url = ha_protocol + "://" + ha_host + ":" + ha_port + "/api/states/" + entity_id
        headers = {
            "Authorization": "Bearer " + ha_token,
            "content-type": "application/json",
        }
        response = get(url, headers=headers)
        response_json = json.loads(response.text)

        # If sensor doesn't exist skips
        if response.status_code == 404:
            continue

        # If sensor is new
        if not os.path.isfile(sensor_data + "/" + entity_id):
            last_reading = [0, time.time()]

            dt = 1
            average = float(response_json['state'])
            energy_ws = average * dt

            file = open(sensor_data + "/" + entity_id, "a")
            file.write("%s;%s;%s\n" % (energy_ws, float(response_json['state']), time.time()))
            file.close()

        # If sensor already exists
        else:
            with open(sensor_data + "/" + entity_id) as f:
                last_energy = f.readlines()[0].split(";")

            # TODO: Take care of long power outage periods
            # Have to take into consideration the possibility of having the device turned off for a long period of time.
            # What happens with the last value of W? Might be misleading. But is it significant?

            dt = time.time() - float(last_energy[2])
            average = (float(response_json['state']) + float(last_energy[1])) / 2
            energy_ws = float(last_energy[0]) + average * dt

            file = open(sensor_data + "/" + entity_id, "w")
            file.write("%s;%s;%s\n" % (energy_ws, float(response_json['state']), time.time()))
            file.close()

            # Converts Ws to kWh
            energy_kwh = energy_ws/3600/1000

            # Posts to Home Assistant the kWh value of the device so it can be read by the Energy Panel
            device_body = {
                "state": energy_kwh,
                "attributes": {
                    "state_class": "total_increasing",
                    "unit_of_measurement": "kWh",
                    "device_class": "energy",
                    "friendly_name": friendly_name
                }
            }
            response = post(url + "_energy", headers=headers, data=json.dumps(device_body))
            if response.status_code != 200:
                print("ERROR SUBMITTING ENERGY OF " + entity_id)
                print("WILL EXIT!")
                exit()

    time.sleep(delta)
