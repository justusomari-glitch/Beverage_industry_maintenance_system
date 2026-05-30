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

## Project Structure

