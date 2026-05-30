# Beverage_industry_maintenance_system

A production-grade predictive maintenance system for beverage plant operations. 
Real-time Kafka sensor streaming across 50 machines in 4 plant sections, 
5-model ML pipeline, MCDM scoring engine, SHAP explainability, and 
LLM-generated maintenance recommendations.

## Live Demo
- **Manual Input (with SHAP):** [https://beverageindustrymaintenancesystem-b4xlh2dyhxtjzmr3hwwepj.streamlit.app/]
- **Real-Time Monitoring:** [https://beverageindustrymaintenancesystem-k3iupzxlon9yukzmxfnadf.streamlit.app/]

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


## Project Stracture
```
Beverage_industry_maintenance_system/
├── .github/
│   └── workflows/
│       └── ci.yaml
├── data and tables/
├── kafka/
│   ├── consumers/
│   │   ├── __pycache__/
│   │   ├── base_consumer.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── packaging_consumer.py
│   │   ├── production_line_consumer.py
│   │   ├── raw_material_consumer.py
│   │   └── utilities_consumer.py
│   └── producers/
│       ├── packaging_producer.py
│       └── production_line_producer.py
├── models/
│   ├── anomaly.pkl
│   ├── failure_type.pkl
│   ├── recommended_action.pkl
│   ├── root_cause_model.pkl
│   └── severity.pkl
├── src/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── llm.py
│   ├── Logger.py
│   ├── models.py
│   ├── predict.py
│   ├── schema.py
│   └── shap_explainer.py
├── tests/
│   ├── __pycache__/
│   ├── test_predict.py
│   └── test_schema.py
├── .dockerignore
├── .env
├── .gitignore
├── ca.pem
├── Dockerfile
├── LICENSE
├── Maintenance_system.ipynb
├── README.md
├── requirements.txt
├── streamlit_manual.py
└── streamlit_real_time.py
```

## Set Up

```bash
git clone https://github.com/justusomari-glitch/Beverage_industry_maintenance_system
cd Beverage_industry_maintenance_system
pip install -r requirements.txt
```

```
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
```
## Screenshots
[View Screenshots](screenshots/)

## Links
- 🔗 [LinkedIn](https://www.linkedin.com/in/justus-kwache-omari/)
- 🚀 [Live Demo - Manual Input](https://beverageindustrymaintenancesystem-b4xlh2dyhxtjzmr3hwwepj.streamlit.app/)
- 📊 [Live Demo - Real Time Monitoring](https://beverageindustrymaintenancesystem-k3iupzxlon9yukzmxfnadf.streamlit.app/)
- 📈 [MLflow Experiments](https://dagshub.com/justusomari-glitch/Beverage_industry_maintenance_system.mlflow)








