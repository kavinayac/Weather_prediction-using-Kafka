import json
import time
import psycopg2
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

while True:
    try:
        consumer = KafkaConsumer(
            'weather',
            bootstrap_servers=['kafka:9092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='weather-group'
        )
        print("Consumer connected to kafka")
        break
    except NoBrokersAvailable:
        print("Kafka not ready for consumer, retrying in 5 secs...")
        time.sleep(5)
        
#postgres
while True:
    try:
        conn = psycopg2.connect(
           dbname="weatherdb",
           user="user",
           password="password",
           host="postgres",
           port="5432"
        )
        cur=conn.cursor()
        break
    except Exception as e:
        print("Postgres not ready, retrying in 5 secs...",)
        time.sleep(5)
        
#create table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        city TEXT,
        temperature FLOAT,
        condition TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

#consume messages
for message in consumer:
    weather=message.value
    try:
        city=weather['location']['name']
        temp=weather['current']['temp_c']
        condition=weather['current']['condition']['text']
        cur.execute(
            "Insert INTO weather_data (city, temperature, condition) VALUES (%s, %s, %s)",
            (city, temp, condition)
        )
        conn.commit()
        print(f"Inserted: {city}, {temp}, {condition}")
    except Exception as e:
        print("Insert error:",e)
