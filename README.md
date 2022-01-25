# W2kWh-home-assistant
## _Generate kWh data from Watt data from your existing devices_

This project aims to create kWh data from sensors that don't generate this data but only output Watt information. The wattage information is retrieved from Home Assistant, processed and written back to Home Assistant in kWh.

When you run this script, the software will read Watt data from Home Assistant and it will create a new sensor on Home Assistant called [name_of_your_sensor]_energy (eg. sensor.ac_kitchen_power -> sensor.ac_kitchen_power_energy) where new kWh data is going to be written. After you'll be able to integrate this sensor to the Energy panel on Home Assistant.

DISCLAIMER: The generated energy information might not be 100% accurate, please use at own discretion!

## Tech

This project was developed using Python 3.8.9 and uses a couple external libraries
- Requests - to make requests to Home Assistant
- Decouple - to read from .env files

## Setup

It is recomended that you have Python 3 installed in your machine.

First of all, clone this repository to your machine.

```sh
git clone https://github.com/rgcouto/W2kWh-home-assistant.git
```

Install the dependencies

```sh
cd W2kWh-home-assistant
pip3 install -r requirements.txt
```

Configure the environment variables. The project includes an example enviroment variables file which you can use. After copying it please fill out the required fields

```sh
cp .env_example .env
vi||nano .env
```

Example below:

```sh
#
# HOME ASSISTANT CONFIGURATIONS
#
HA_TOKEN=eyJ0eXaSDQV1QiLCJhbGciOiJIUzI1NiJ9.AasdaSDqwEqDWeFeGtrhWEFShYjTYRhGASDfaGwER.SPSON3KUHmEhSyWeh7e0vIcz9110AE5wZtzqFQ6giA4
HA_PROTOCOL=http
HA_HOST=192.168.4.100
HA_PORT=8123

#
# READING/WRITING SLEEP DELTA IN SECONDS
#   Every X seconds a Watt is readed and a kWh is written
DELTA=5

#
# SENSORS LIST
#   USAGE: entity_id_1,friendly_name;entity_id_2,friendly_name (friendly name without spaces)
ENTITIES=ac_living_room_power,AC-Living-Room;ac_masterbedroom_power,AC-Master-Bedroom

```

NOTE: Please notice that the provided credentials are fake and should be replaced by proper and existing ones.

When everything is correctly setup, start the script
```sh
python3 main.py 2>&1 &
```


## Development

Want to contribute? Great! Feel free to submit a Pull Request!


## License
MIT