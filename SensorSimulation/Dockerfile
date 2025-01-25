FROM python:3.11-slim as build
WORKDIR ./
COPY . .
RUN pip3 install paho-mqtt
CMD ["python3", "mqtt-publisher.py"]