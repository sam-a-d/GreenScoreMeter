import paho.mqtt.client as mqtt
import random
import time
import configparser
import threading

from simulator import Sensor


# Load MQTT configuration from file
# config = configparser.ConfigParser()
# config.read('config.ini')

# client_address = config['mqtt']['client_address']
client_address = 'localhost'
# port = int(config['mqtt']['port'])
port = 1883
areas = 1
homes = 2
sensors = ['electricity', 'water', 'natural_gas', 'air_pollution', 'crude_oil',\
           'solarProduction', 'hydrologicalProduction', 'windProduction', 'bioGasProduction'\
            ]

# forests = int(config['data_generation']['forests'])
# areas = int(config['data_generation']['areas'])
# time_sleep = int(config['data_generation']['time_sleep'])
# sensors = config['data_generation']['sensors'].split('|')

mqtt_client = mqtt.Client()
mqtt_client.connect(client_address, port=port)
dataSimulator = Sensor()

def publish_area_data(mqtt_client, sensors, area, home):
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

            topic = f"{sensor}/area_{area}/home_{home}"
            mqtt_client.publish(topic, f'{{"{sensor}":{data}}}')
            print(f"Published {topic}: {data}")

        time.sleep(1)  # Breaks between publishing data (defined in config)
        # Uncomment the line below if you want to see the published data in the console
        print(f"Published {sensor} data: {data}")

# Publish data for each sensor
threads=[]
for area in range(areas):
    for home in range(homes):
        thread = threading.Thread(target=publish_area_data, args=(mqtt_client, sensors, area, home))
        threads.append(thread)
        thread.start()

# Wait for all threads to complete (which they won't, as they're infinite loops)
for thread in threads:
    thread.join()