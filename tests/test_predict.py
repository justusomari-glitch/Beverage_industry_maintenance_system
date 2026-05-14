from fastapi.testclient import TestClient
from src.predict import app

client= TestClient(app)

valid_payload={
    "temperature": 75.0,
    "vibration": 1,
    "pressure": 10,
    "rotation_speed": 1400,
    "torque": 50,
    "voltage": 230.0,
    "current": 20,
    "power_consumption": 20,
    "humidity": 70,
    "noise_level": 73.2,
    "flow_rate": 13.5,
    "product_temperature": 44.2,
    "cleaning_cycle_status": 1,
    "oil_level": 80,
    "bearing_temperature": 60.9,
    "hours_since_maintenance": 6,
    "zone": "Zone A",
    "criticality_level": "Low"
}

def test_home():
    response=client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_predict_status_code():
    response=client.post("/predict",json=valid_payload)
    assert response.status_code == 200

def test_predict_response_keys():
    response=client.post("/predict",json=valid_payload)
    data=response.json()
    assert "anomaly" in data
    assert "failure_type" in data
    assert "severity" in data
    assert "priority" in data
    assert "mcdm_score" in data
    assert "recommended_action" in data
    assert "root_cause" in data

def test_predict_invalid_payload():
    response=client.post("/predict",json={})
    assert response.status_code == 422

def test_predict_anomaly_is_binary():
    response=client.post("/predict",json=valid_payload)
    assert response.json()['anomaly'] in [0,1]
    

