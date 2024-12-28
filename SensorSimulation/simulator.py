import paho.mqtt.client as mqtt
import random
import time
import configparser
import threading


# Load MQTT configuration from file
# config = configparser.ConfigParser()
# config.read('config.ini')

# client_address = config['mqtt']['client_address']
client_address = 'localhost'
# port = int(config['mqtt']['port'])
port = 1883
areas = 1
homes = 2
sensors = ['electricity']

# forests = int(config['data_generation']['forests'])
# areas = int(config['data_generation']['areas'])
# time_sleep = int(config['data_generation']['time_sleep'])
# sensors = config['data_generation']['sensors'].split('|')

mqtt_client = mqtt.Client()
mqtt_client.connect(client_address, port=port)

def publish_area_data(mqtt_client, sensors, area, home):
    while True:
        # Generate random sensor data
        for sensor in sensors:
            if sensor == 'electricity':
                data = round(random.uniform(0, 40), 2)  # Simulating temperature between 0 to 40 degrees Celsius
            # elif sensor == 'humidity':
            #     data = round(random.uniform(30, 70), 2)  # Simulating humidity between 30% to 70%
            # elif sensor == 'light_intensity':
            #     data = random.randint(0, 1000)  # Simulating light intensity between 0 to 1000
            # elif sensor == 'air_quality':
            #     data = random.randint(0, 500)  # Simulating air quality index between 0 to 500
            # -----> don't uncomment this -->  mqtt_client.publish(topic, payload=str(data))
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