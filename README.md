# Beverage_industry_maintenance_system

A production-grade predictive maintenance system for beverage plant operations. 
Real-time Kafka sensor streaming across 50 machines in 4 plant sections, 
5-model ML pipeline, MCDM scoring engine, SHAP explainability, and 
LLM-generated maintenance recommendations.

## Live Demo
- **Manual Input (with SHAP):** [link]
- **Real-Time Monitoring:** [link]

## System Architecture

### Two Modes of Operation

**Manual Input**
- Technician enters sensor readings manually
- ML pipeline returns instant prediction
- SHAP explains which features drove the prediction
- LLM generates plain-language maintenance recommendation

**Live Monitoring**
- 4 Kafka topics stream real-time sensor data (one per section)
- Per-section dashboard updates every 15 seconds
- Displays all machines with current status, failure type, severity, 
  MCDM score, and LLM recommendation
- SHAP omitted by design — impractical at 50-machine, 15s refresh rate

## Plant Sections & Kafka Topics

| Section | Kafka Topic |
|---|---|
| Packaging | sensors.packaging |
| Production Line | sensors.production-line |
| Raw Material Processing | sensors.raw-material-processing |
| Utilities | sensors.utilities |

## ML Pipeline (5 Models)

| Model | Output |
|---|---|
| Anomaly Detection | Anomaly flag (Isolation Forest) |
| Failure Type | Classification (XGBoost + Random Forest) |
| Severity Scoring | High / Medium / Low |
| Root Cause | Root cause identification |
| Recommended Action | Rule-based action output |

All models unified via **MCDM scoring engine** into a single priority score 
per machine.


## Tech Stack

| Layer | Technology |
|---|---|
| ML | scikit-learn, XGBoost, SHAP |
| Streaming | Confluent Cloud Kafka |
| API | FastAPI (EC2) |
| Frontend | Streamlit |
| Database | Aiven MySQL |
| LLM | Groq |
| Experiment Tracking | MLflow + DagsHub |
| CI/CD | GitHub Actions |
| Containerization | Docker |

## Setup

```bash
git clone https://github.com/justusomari-glitch/Beverage_industry_maintenance_system
cd Beverage_industry_maintenance_system
pip install -r requirements.txt


DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=
SSL_CA_CERT=ca.pem
KAFKA_BOOTSTRAP_SERVERS=
KAFKA_API_KEY=
KAFKA_API_SECRET=
GROQ_API_KEY=
FASTAPI_URL=




