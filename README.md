# Weather Prediction using Kafka

A simple example project that demonstrates building a streaming pipeline for weather data using Apache Kafka and Python. The repository contains producers and consumers that ingest weather data, stream it through Kafka topics, and run prediction/modeling components. This README provides setup and run instructions — adjust paths and commands to match the repository structure.

## Features

- Ingest weather data (CSV / API) with a Kafka producer
- Stream processing with Kafka consumers
- Model training and prediction components (offline and streaming)
- Dockerfile to containerize services

## Architecture

Typical components in this repo:

- Producer: reads raw weather data (files or APIs) and publishes messages to a Kafka topic
- Kafka: message broker for decoupled streaming
- Consumer: subscribes to topics, processes messages, and runs predictions or stores processed data
- Model: training scripts and model artifacts used for batch or online prediction

A simple flow:

1. Producer publishes raw weather records to a Kafka topic (e.g. `weather.raw`).
2. Consumer reads from `weather.raw`, preprocesses, and either stores results or forwards to `weather.processed`.
3. Prediction service consumes `weather.processed` and produces predictions to `weather.predictions`.

## Requirements

- Python 3.8+
- Kafka (Apache Kafka or Confluent Platform)
- Docker (optional, for containerized setup)
- Common Python libraries: pandas, numpy, scikit-learn (or your ML framework), kafka-python or confluent-kafka

Install Python dependencies with:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

If the repository does not include `requirements.txt`, install typical packages:

```bash
pip install pandas numpy scikit-learn kafka-python confluent-kafka
```

## Running Kafka locally (Docker Compose example)

Use a small Docker Compose file to start Zookeeper and Kafka. Create `docker-compose.yml` if not present and run:

```bash
docker compose up -d
```

Example Docker images: `confluentinc/cp-zookeeper` and `confluentinc/cp-kafka`. Adjust advertised listeners as needed for your environment.

## Running the project (example commands)

Start Kafka (see previous section). Then run the producer and consumer scripts. Replace the filenames with the actual scripts in the repo:

```bash
# Start the producer that reads sample data and publishes to Kafka
python producer.py --topic weather.raw --bootstrap-server localhost:9092 --input data/sample_weather.csv

# Start the consumer that reads, preprocesses and/or predicts
python consumer.py --topic weather.raw --bootstrap-server localhost:9092

# Run a model training script (if present)
python train_model.py --data data/training.csv --output models/weather_model.pkl
```

To build and run the Docker image (if Dockerfile is provided):

```bash
docker build -t weather-kafka:latest .
# Run container
docker run --env-file .env -p 8080:8080 weather-kafka:latest
```

## Configuration

Use environment variables or a configuration file to store Kafka bootstrap servers, topics, and model paths. Example `.env` values:

```
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
WEATHER_TOPIC_RAW=weather.raw
WEATHER_TOPIC_PROCESSED=weather.processed
MODEL_PATH=models/weather_model.pkl
```

## Project structure (example)

- producer.py         # Publishes weather messages to Kafka
- consumer.py         # Consumes messages and runs processing/prediction
- train_model.py      # Offline model training
- models/             # Saved model artifacts
- data/               # Example input CSV files
- Dockerfile
- docker-compose.yml

## Troubleshooting

- If producers cannot connect: ensure Kafka is running and `KAFKA_BOOTSTRAP_SERVERS` is set correctly.
- Topic not found: create the topic manually or configure your producer to auto-create topics.
- Permissions / network errors: check advertised listeners and Docker networking if running Kafka in containers.


