import pymysql
from config import DB_CONFIG

def get_db_connection():
    return pymysql.connect(
        **DB_CONFIG,
        cursorclass=pymysql.cursors.DictCursor
    )

def create_table(conn,table_name):
    cursor=conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            machine_id VARCHAR(255),
            machine_name VARCHAR(255),
            machine_type VARCHAR(255),
            section VARCHAR(255),
            timestamp DATETIME,
            -- Sensor Data
            temperature FLOAT,
            vibration FLOAT,
            pressure FLOAT,
            rotation_speed FLOAT,
            torque FLOAT,
            voltage FLOAT,
            current FLOAT,
            power_consumption FLOAT,
            humidity FLOAT,
            noise_level FLOAT,
            flow_rate FLOAT,
            product_temperature FLOAT,
            cleaning_cycle_status INT,
            oil_level FLOAT,
            bearing_temperature FLOAT,
            hours_since_maintenance INT,
            zone VARCHAR(255),
            criticality_level VARCHAR(255),
            -- Prediction and Analysis
            anomaly BOOLEAN,
            failure_type VARCHAR(255),
            recommended_action TEXT,
            root_cause TEXT,
            severity VARCHAR(255),
            mcdm_score FLOAT,
            priority VARCHAR(255),
            system_explanations TEXT,
            system_recommendations TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()

def save_to_db(conn,table_name,payload,prediction):
    cursor=conn.cursor()
    query=f"""
        INSERT INTO {table_name} (machine_id, machine_name, machine_type, section,
        timestamp,temperature,vibration,pressure,rotation_speed,torque,voltage,current,
        power_consumption,humidity,noise_level,flow_rate,product_temperature,cleaning_cycle_status,
        oil_level,bearing_temperature,hours_since_maintenance,zone,criticality_level,anomaly,failure_type,
        recommended_action,
        root_cause,severity,mcdm_score,priority,system_explanations,system_recommendations)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values= (
        payload["machine_id"],
        payload["machine_name"],
        payload["machine_type"],
        payload["section"],
        payload["timestamp"],
        payload.get("temperature"),
        payload.get("vibration"),
        payload.get("pressure"),
        payload.get("rotation_speed"),
        payload.get("torque"),
        payload.get("voltage"),
        payload.get("current"),
        payload.get("power_consumption"),
        payload.get("humidity"),
        payload.get("noise_level"),
        payload.get("flow_rate"),
        payload.get("product_temperature"),
        payload.get("cleaning_cycle_status"),
        payload.get("oil_level"),
        payload.get("bearing_temperature"),
        payload.get("hours_since_maintenance"),
        payload.get("zone"),
        payload.get("criticality_level"),
        prediction.get("anomaly"),
        prediction.get("failure_type"),
        prediction.get("recommended_action"),
        prediction.get("root_cause"),
        prediction.get("severity"),
        prediction.get("mcdm_score"),
        prediction.get("priority"),
        prediction.get("system_explanations"),
        prediction.get("system_recommendations")
    )
    cursor.execute(query, values)
    conn.commit()
    cursor.close()