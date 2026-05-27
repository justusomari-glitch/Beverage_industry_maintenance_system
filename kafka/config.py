import os
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path

load_dotenv()
KAFKA_CONFIG= {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVER"),
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": os.getenv("KAFKA_API_KEY"),
    "sasl.password": os.getenv("KAFKA_API_SECRET")

}
DB_CONFIG={
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "ssl": {"ca": os.getenv("SSL_CA_CERT")},
    "cursorclass": "pymysql.cursors.DictCursor"
}
TOPICS = {
    "Packaging": "sensors.packaging",
    "Production Line": "sensors.production-line",
    "Raw Material Processing": "sensors.raw-material-processing",
    "Utilities": "sensors.utilities"
}

FASTAPI_URL = os.getenv("FASTAPI_URL")

BASE_DIR= Path(__file__).resolve().parent.parent
MACHINES_DF= pd.read_csv(BASE_DIR/"data and tables"/"machines.csv")