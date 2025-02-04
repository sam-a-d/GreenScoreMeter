import paho.mqtt.client as mqtt
import time
import configparser
import threading

from simulator import Sensor

import csv
import ast

csvFilepath="/data/setting/config.csv"
homesRecord="/data/homes/homes.csv"

config = configparser.ConfigParser()
config.read('simulatorConf.ini')

homes = dict()

with open(homesRecord, 'r') as hRecord:
    reader = csv.DictReader(hRecord)
    for row in reader:
        if row['Area'] not in homes.keys():
            homes[row['Area']] = list()

        homes[row['Area']].append(row['House'])

client_address = config['mqtt_setting']['client_address']
port = int(config['mqtt_setting']['port'])


sensors = ['electricity', 'water', 'natural_gas', 'air_pollution', 'crude_oil',\
           'solarProduction', 'hydrologicalProduction', 'windProduction', 'bioGasProduction'\
            ]

dataSimulator = Sensor()

def create_client():
    client = mqtt.Client()
    client.connect(client_address, port=port)
    return client


# Initialize a resource production range dictionary that store range data 
res_prod_rngs = {}

def convert_range(value):
    """Convert range string from '(min-max)' to a tuple (min, max)"""
    value = value.strip("() ")  # Remove parentheses and extra spaces
    min_val, max_val = map(float, value.split('-'))  # Convert to float
    return (min_val, max_val)

with open(csvFilepath, 'r') as confFile:
    reader = csv.DictReader(confFile)
    for row in reader:
        if '_range' in row['property']:
            res_prod_rngs[row['property']] = convert_range(row['value'])



def publish_area_data(sensors, area, home):

    mqtt_client = create_client()  # Create a new client for each thread

    while True:
        # Generate random sensor data
        for sensor in sensors:
            if sensor == 'electricity':
                data = dataSimulator.getElectricity(res_prod_rngs['electricity_range']) if (val := res_prod_rngs.get('electricity_range')) else dataSimulator.getElectricity()
            elif sensor == 'water':
                data = dataSimulator.getWater(res_prod_rngs['water_range']) if (val := res_prod_rngs.get('water_range')) else dataSimulator.getWater()
            elif sensor == 'natural_gas':
                data = dataSimulator.getNaturalGas(res_prod_rngs['natural_gas_range']) if (val := res_prod_rngs.get('natural_gas_range')) else dataSimulator.getNaturalGas()
            elif sensor == 'air_pollution':
                data = dataSimulator.getAirPollution(res_prod_rngs['air_pollution_range']) if (val := res_prod_rngs.get('air_pollution_range')) else dataSimulator.getAirPollution()
            elif sensor == 'crude_oil':
                data = dataSimulator.getCrudeOil(res_prod_rngs['crude_oil_range']) if (val := res_prod_rngs.get('crude_oil_range')) else dataSimulator.getCrudeOil()
            elif sensor == 'solarProduction':
                data = dataSimulator.getSolarProduction()
            elif sensor == 'hydrologicalProduction':
                data = dataSimulator.getHydrologicalProduction()
            elif sensor == 'windProduction':
                data = dataSimulator.getWindProduction()
            elif sensor == 'bioGasProduction':
                data = dataSimulator.getBioGasProduction()

            topic = f"sensor/{sensor}/area_{area}/home_{home}"
            mqtt_client.publish(topic, f'{{"{sensor}":{data}}}')
            # print(f"Published {topic}: {data}")

        time.sleep(1)  

# Publish data for each sensor
threads=[]

for area, houses in homes.items():
    for home in houses:
        thread = threading.Thread(target=publish_area_data, args=(sensors, area, home))
        threads.append(thread)
        thread.start()

for thread in threads:
    thread.join()