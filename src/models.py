import joblib
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

# shap is slow so we are trying to compute it on load
from src.shap_explainer import init_anomaly_explainer,init_failure_explainer
import shap
def anomaly_scorer(estimator,X):
    X_transformed=estimator.named_steps['processing'].transform(X)
    return estimator.named_steps['ir'].score_samples(X_transformed).mean()


models_loaded= False
anomaly_model= None
failure_model=None
recommendation_model=None
root_cause_model=None
severity_model=None
anomaly_explainer=None
failure_explainer=None


def load_models():
    global anomaly_model,failure_model,recommendation_model,root_cause_model,severity_model,models_loaded,anomaly_explainer,failure_explainer
    anomaly_model=joblib.load('models/anomaly.pkl')
    failure_model=joblib.load('models/failure_type.pkl')
    recommendation_model=joblib.load('models/recommended_action.pkl')
    root_cause_model=joblib.load('models/root_cause_model.pkl')
    severity_model=joblib.load('models/severity.pkl')
    best_pipeline=anomaly_model.best_estimator_
    anomaly_explainer=shap.TreeExplainer(best_pipeline.named_steps['ir'])
    rf_model=failure_model.named_steps['ensemble'].estimators_[0]
    xg_model=failure_model.named_steps['ensemble'].estimators_[1]
    rf_explainer=shap.TreeExplainer(rf_model)
    xg_explainer=shap.TreeExplainer(xg_model)
    failure_explainer=(rf_explainer,xg_explainer)
    models_loaded = True

print("Models loaded successfully")