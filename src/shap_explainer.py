import shap
import numpy as np


def init_anomaly_explainer(anomaly_model):
    best_pipeline=anomaly_model.best_estimator_
    explainer=shap.TreeExplainer(best_pipeline.named_steps['ir'])
    return explainer
def get_shap_anomaly_explanation(anomaly_model,anomaly_explainer, df):
    # Create a shap Explainer for the anomaly detection mode which is Isoation Forest
    # get the best pipeline from anomaly
    best_pipeline=anomaly_model.best_estimator_
    #trasform data using processing steps
    input_array=best_pipeline.named_steps['processing'].transform(df)
    #get the feature names from the column transformer
    feature_names=best_pipeline.named_steps['processing'].get_feature_names_out()
    #clean the feature names by removing 'std'
    feature_names=[f.replace('std_',"")for f in feature_names]
    # tree explainer on isolation forest
    shap_values=anomaly_explainer.shap_values(input_array,approximate=True)
    vals=np.array(shap_values)
    #return as a dict
    return dict(zip(feature_names,vals[0][0].tolist()))

def init_failure_explainer(failure_model):
    rf_model=failure_model.named_steps['ensemble'].estimators_[0]
    xg_model=failure_model.named_steps['ensemble'].estimators_[1]
    rf_explainer=shap.TreeExplainer(rf_model)
    xg_explainer=shap.TreeExplainer(xg_model)
    return rf_explainer,xg_explainer

def get_shap_failure_explanation(failure_model,failure_explainer,df):
    rf_explainer,xg_explainer=failure_explainer

    input_array=failure_model.named_steps['type_process'].transform(df)
    input_array=failure_model.named_steps['type_features'].transform(input_array)
    feature_names=failure_model.named_steps['type_process'].get_feature_names_out()
    feature_names=[f.replace('oht',"").replace('std_',"")for f in feature_names]
    rf_shap=rf_explainer.shap_values(input_array,approximate=True)
    xg_shap=xg_explainer.shap_values(input_array,approximate=True)

    avg_shap=(np.array(rf_shap)+np.array(xg_shap))/2
    return dict(zip(feature_names,avg_shap[0][0].tolist()))
    

