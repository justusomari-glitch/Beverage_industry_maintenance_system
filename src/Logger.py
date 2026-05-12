import dagshub
import os
import mlflow
from dotenv import load_dotenv

load_dotenv()

EXPERIMENT_NAME="Beverage_Industry_Maintenance"

def setup_mlflow():
    try:
        dagshub_token=os.getenv('DAGSHUB_TOKEN')
        os.environ['MLFLOW_TRACKING_USERNAME']=os.getenv('MLFLOW_TRACKING_USERNAME')
        os.environ['MLFLOW_TRACKING_PASSWORD']=dagshub_token
        dagshub.init(
            repo_owner="justusomari-glitch",
            repo_name="Beverage_industry_maintenance_system",
            mlflow=True
        )
        mlflow.set_experiment(EXPERIMENT_NAME)
        print("Mlflow setup succesful")
    except Exception as e:
        print(f"Mlflow setup warning: {e}")
    

def log_prediction(df,anomaly_binary,failure_type,recommended_action,root_cause,tuned_severity,scores,
        priority,anomaly_shap,failure_type_shap):
    
    try:
        with mlflow.start_run():
            print("1-Starting param-logs")
            mlflow.log_params(df.to_dict(orient='records')[0])
            mlflow.set_tags({
                "anomaly": anomaly_binary,
                "failure_type": failure_type,
                "recommended_action": recommended_action,
                "root_cause": root_cause,
                "severity": tuned_severity,
                "priority": priority
            })
            print("Params loaded")
            mlflow.log_metric("mcdm_score", round(float(scores), 2),)
            print("Metric Loaded")
            mlflow.log_dict({
                "anomaly_explanation":anomaly_shap,
                "failure_type_explanation":failure_type_shap
            },"explanations.json")
            print("shap loaded")
    except Exception as e:
        print(f"Mlflow Error: {e}")
            
