import json
import requests
from confluent_kafka import Consumer, KafkaError
from config import KAFKA_CONFIG, TOPICS, FASTAPI_URL
from db import get_db_connection, create_table, save_to_db
import traceback


MODEL_FEATURES=[
    "temperature",
    "vibration",
    "pressure",
    "rotation_speed",
    "torque",
    "voltage",
    "current",
    "power_consumption",
    "humidity",
    "noise_level",
    "flow_rate",
    "product_temperature",
    "cleaning_cycle_status",
    "oil_level",
    "bearing_temperature",
    "hours_since_maintenance",
    "zone",
    "criticality_level"
]
METADATA_FIELDS=[
    "machine_id",
    "machine_name",
    "machine_type",
    "section",
    "timestamp"
]

def run(topic,group_id,table_name):
    conn= get_db_connection()
    create_table(conn,table_name)

    consumer_config = {
        **KAFKA_CONFIG,
        "group.id": group_id,
    }
    consumer=Consumer(consumer_config)
    consumer.subscribe([topic])
    print(f"Consumer started for topic :{topic}| table:{table_name}")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Error: {msg.error()}")
                    break
                

            payload = json.loads(msg.value().decode("utf-8"))
            print(f"Received message: {payload}")
            payload["cleaning_cycle_status"]=1 if payload.get("cleaning_cycle_status")=="Active" else 0

            model_input = {k: payload[k] for k in MODEL_FEATURES if k in payload}
            metadata = {k: payload[k] for k in METADATA_FIELDS if k in payload}


            model_input["cleaning_cycle_status"] = 1 if model_input.get("cleaning_cycle_status") == "Active" else 0
            try:
                response = requests.post(FASTAPI_URL, json=model_input)
                prediction = response.json()
                print(f"Prediction response: {prediction}")
                
                save_to_db(conn,table_name,payload,prediction)
                print(f"Saved -machine_id={payload.get('machine_id')}|table={table_name}")
            except Exception as e:
                traceback.print_exc()
                print(f"Error calling prediction API: {e}")
    except KeyboardInterrupt:
        print("Consumer interrupted. Closing connection.")
    finally:
        consumer.close()    
        conn.close()


   
               
                