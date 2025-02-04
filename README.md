# Green Score Meter

The **Green Score Meter** is an IoT-based system designed to promote sustainability in smart cities by monitoring energy consumption, renewable energy production, and air pollution levels. It calculates a **Green Score** for each household, helping authorities and individuals track and optimize their environmental impact.

## Features

- **Real-time Monitoring:** Collects and analyzes data on electricity, water, gas usage, and air pollution.
- **Green Score Calculation:** Assigns a sustainability score to households based on energy efficiency.
- **Visualization Dashboard:** Provides interactive insights using **Grafana**.
- **MQTT-based Communication:** Uses **MQTT** for efficient data transmission.
- **Dockerized System:** Simplifies deployment and scalability.

## Tech Stack

- **Node-RED** - IoT data processing
- **MQTT Broker** - Message communication
- **InfluxDB** - Time-series database for sensor data storage
- **Grafana** - Data visualization
- **Docker** - Containerized deployment
- **Python** - Sensor simulation

## Installation & Setup

### Prerequisites

- **Docker** & **Docker Compose** installed on your system.

### Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/sam-a-d/GreenScoreMeter.git
   cd GreenScoreMeter
   ```
2. Run the system using Docker:
   ```sh
   docker-compose up
   ```
3. Access services:
   - **Node-RED UI**: `http://localhost:1880`
   - **Grafana Dashboard**: `http://localhost:3000`
   - **MQTT Broker**: `mqtt://localhost:1883`
   - **InfluxDB**: `http://localhost:8086`

## Usage

1. **Configure Sensor Simulation**
   - Edit `config.csv` to define household metrics configurations.
2. **Monitor Live Data**
   - View live sensor readings on Grafana.
3. **Analyze Green Score**
   - Green Scores are updated in the dashboard based on resource usage.

---
**Developed as part of the SE4GD Master's Degree Programme**
