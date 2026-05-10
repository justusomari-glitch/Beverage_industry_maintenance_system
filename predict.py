from fastapi import FastAPI 
import pandas as pd
import numpy as np
# building the schema for input of data
from src.schema import MaintenanceSystem
# loading models
from src.models import  anomaly_scorer
from src import models as model_store
from src.models import load_models, anomaly_model, failure_model, recommendation_model, root_cause_model, severity_model
import sys
# this is integration of the MCDM
from src.mcdm import tune_severity,compute_mcdm_score, decision_engine
#shap intergration
from src.shap_explainer import get_shap_anomaly_explanation,get_shap_failure_explanation


sys.modules['__main__'].anomaly_scorer = anomaly_scorer



app =FastAPI()
load_models()  # Ensure models are loaded on startup

@app.get("/")
def home():
    return{"message":"Welcome to the Beverage Industry Maintenance System API"}

@app.post("/predict")
def predict(maintenance_data: MaintenanceSystem):
    
    anomaly_model=model_store.anomaly_model
    failure_model=model_store.failure_model
    recommendation_model=model_store.recommendation_model
    root_cause_model=model_store.root_cause_model
    severity_model=model_store.severity_model

    print("Models loaded successfully in predict function")
    # Convert the input data to a pandas DataFrame
    input_dict= maintenance_data.model_dump()
    df = pd.DataFrame([input_dict])

    # Make predictions using the loaded models
    anomaly = anomaly_model.predict(df)[0]
    anomaly_binary=int(np.where(anomaly==-1,1,0))
    failure_type = failure_model.predict(df)[0]
    recommended_action = recommendation_model.predict(df)[0]
    root_cause = root_cause_model.predict(df)[0]
    severity = severity_model.predict(df)[0]

    # Building the MCDM
    scores=compute_mcdm_score(anomaly,failure_type,recommended_action,root_cause,severity)
    row={
        "anomaly": anomaly_binary,
        "failure_type": failure_type,
        "recommended_action": recommended_action,
        "root_cause": root_cause,
        "severity": severity,
        "mcdm_score": scores
    }
    tuned_severity=tune_severity(row)
    row['severity']=tuned_severity
    priority=decision_engine(row)

    #shap explainability
    anomaly_shap=get_shap_anomaly_explanation(model_store.anomaly_model,model_store.anomaly_explainer, df)
    failure_type_shap=get_shap_failure_explanation(model_store.failure_model,model_store.failure_explainer,df)

    return {
        "anomaly": anomaly_binary,
        "failure_type": failure_type,
        "recommended_action": recommended_action,
        "root_cause": root_cause,
        "severity": tuned_severity,
        "mcdm_score": round(float(scores), 2),
        "priority": priority,
        "explanations":{
            "anomaly_explanation":anomaly_shap,
            "failure_type_explanation":failure_type_shap
        }

    }
