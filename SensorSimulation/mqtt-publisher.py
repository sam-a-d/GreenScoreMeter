import paho.mqtt.client as mqtt
import time
import configparser
import threading

from simulator import Sensor

import csv
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

# port = 1883
# areas = 2
# homes = 10

sensors = ['electricity', 'water', 'natural_gas', 'air_pollution', 'crude_oil',\
           'solarProduction', 'hydrologicalProduction', 'windProduction', 'bioGasProduction'\
            ]

# This limit is suppose to set by the appropriate authority
resouceUsageLimits = {
    'electricity': 500,
    'water': 700,
    'natural_gas': 0.6,
    'air_pollution': 300,
    'crude_oil' : 70
}

# forests = int(config['data_generation']['forests'])
# areas = int(config['data_generation']['areas'])
# time_sleep = int(config['data_generation']['time_sleep'])
# sensors = config['data_generation']['sensors'].split('|')

# mqtt_client = mqtt.Client()
# mqtt_client.connect(client_address, port=port)
dataSimulator = Sensor()

def create_client():
    client = mqtt.Client()
    client.connect(client_address, port=port)
    return client


def publish_area_data(sensors, area, home):

    mqtt_client = create_client()  # Create a new client for each thread

    while True:
        # Generate random sensor data
        for sensor in sensors:
            if sensor == 'electricity':
                data = dataSimulator.getElectricity()
            elif sensor == 'water':
                data = dataSimulator.getWater()
            elif sensor == 'natural_gas':
                data = dataSimulator.getNaturalGas()
            elif sensor == 'air_pollution':
                data = dataSimulator.getAirPollution()
            elif sensor == 'crude_oil':
                data = dataSimulator.getCrudeOil()
            elif sensor == 'solarProduction':
                data = dataSimulator.getSolarProductionPercentage()
            elif sensor == 'hydrologicalProduction':
                data = dataSimulator.getHydrologicalProductionPercentage()
            elif sensor == 'windProduction':
                data = dataSimulator.getWindProductionPercentage()
            elif sensor == 'bioGasProduction':
                data = dataSimulator.bioGasProductionPercentage()

            topic = f"sensor/{sensor}/area_{area}/home_{home}"
            mqtt_client.publish(topic, f'{{"{sensor}":{data}}}')
            print(f"Published {topic}: {data}")

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