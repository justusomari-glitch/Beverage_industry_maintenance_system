import json
import time
import sys
import random
from pathlib import Path
from datetime import datetime,timezone
from confluent_kafka import Producer


sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import KAFKA_CONFIG,TOPICS,MACHINES_DF

RAW_MATERIAL_MACHINES=MACHINES_DF[
    MACHINES_DF['section'] == "Raw Material Processing"
].to_dict("records")

def simulate_sensors():
    return {
        "temperature": round(random.uniform(20.0,120),2),
        "vibration": round(random.uniform(0.1,10.0),2),
        "pressure": round(random.uniform(1.0,20.0),2),
        "rotation_speed": round(random.uniform(1000.0,2000.0),2),
        "torque": round(random.uniform(50.0,200.0),2),
        "voltage": round(random.uniform(220.0,400.0),2),
        "current": round(random.uniform(5.0,40.0),2),
        "power_consumption": round(random.uniform(10.0,50.0),2),
        "humidity": round(random.uniform(30.0,90.0),2),
        "noise_level": round(random.uniform(40.0,100.0),2),
        "flow_rate": round(random.uniform(200.0,500.0),2),
        "oil_level": round(random.uniform(0.0,100.0),2),
        "bearing_temperature": round(random.uniform(30.0,100.0),2),
        "product_temperature": round(random.uniform(20.0,80.0),2),
        "cleaning_cycle_status": random.choice(["Active", "Inactive"]),
        "hours_since_maintenance": round(random.uniform(0.0,200.0),2),
        "zone": random.choice(["Zone A", "Zone B", "Zone C"]),
        "criticality_level": random.choice(["Low", "Medium", "High"])
    }

def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [partition {msg.partition()}]")

def run():
    producer = Producer(KAFKA_CONFIG)
    topic=TOPICS['Raw Material Processing']
    print(f"Raw Material Processing Producer Started - {len(RAW_MATERIAL_MACHINES)} machines sending data to topic '{topic}'")

    while True:
        for machine in RAW_MATERIAL_MACHINES:
            payload = {
                #metadata
                "machine_id": machine['machine_id'],
                "machine_name": machine['machine_name'],
                "machine_type": machine['machine_type'],
                "section": machine['section'],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                # Sensor data
                **simulate_sensors()
            }
            producer.produce(
                topic=topic,
                value=json.dumps(payload),
                callback=delivery_report,
                key=str(machine['machine_id'])
            )
            producer.poll(0)
            time.sleep(5)
        producer.flush()
        print(f"Cycle complete. Waiting for next cycle...")
        time.sleep(10)
if __name__ == "__main__":
    run()