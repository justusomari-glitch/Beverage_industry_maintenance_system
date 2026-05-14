import pytest
from pydantic import ValidationError
from src.schema import MaintenanceSystem,ChatRequests

#Valid Base input 
valid_input={
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
def test_valid_input():
    m=MaintenanceSystem(**valid_input)
    assert m.temperature == 75.0

def test_missing_required_field():
    bad=valid_input.copy()
    del bad['temperature']
    with pytest.raises(ValidationError):
        MaintenanceSystem(**bad)

def test_wrong_type_float_field():
    bad=valid_input.copy()
    bad['temperature']="hot"
    with pytest.raises(ValidationError):
        MaintenanceSystem(**bad)

def test_wrong_type_int_field():
    bad=valid_input.copy()
    bad['cleaning_cycle_status']="hot"
    with pytest.raises(ValidationError):
        MaintenanceSystem(**bad)

def test_chat_request_valid():
    c= ChatRequests(user_message="What Is Wrong?",
                    prediction_context={})
    assert c.user_message=="What Is Wrong?"
    assert c.conversation_history==[]

def test_chat_request_missing_message():
    with pytest.raises(ValidationError):
        ChatRequests()





