import json
import time
import requests
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

API_KEY = '7eeae7baa5314a419e144709262101'
CITY = 'Chennai'
URL=f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no"

while True:
    try:
        producer=KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Producer connected to kafka")
        break
    except NoBrokersAvailable:
        print("Kafka not ready forproducer,retrying...")
        time.sleep(5)
        
while True:
    try:
        response=requests.get(URL)
        data=response.json()
        producer.send('weather',value=data)
        producer.flush()
        print("Sent weather data:",data['current']['temp_c'])
        time.sleep(10)
        
    except Exception as e:
        print("Producer error:",e)


