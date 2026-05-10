import numpy as np

severity_weights={
    'High':1.0,
    'Medium':0.7,
    'Low':0.2
}

failure_weights={
    'No Failure':0.2,
    'Pressure Leak':0.7,
    'Electrical Fault':0.8,
    'Valve Failure':0.7,
    'Overheating':1.0,
    'Bearing Failure':1.0,
    'Belt Wear':0.6,
    'Motor Failure':0.7,
    'Lubrication Failure':0.5,
    'Pump Cavitation':0.6,
    'Compressor Surge':0.6
}

root_cause_weights={
    'No Fault Detected':0.2,
    'Normal wear and tear':0.5,
    'Moisture ingress':0.4,
    'Corrosion due to moisture':0.4,
    'Seal degradation':0.7,
    'Overloading':0.6,
    'Voltage fluctuation':0.8,
    'Loose connections':0.6,
    'High ambient temperature':0.7,
    'Short circuit':0.9,
    'Poor lubrication':0.8,
    'Blocked cooling vents':0.6,
    'Misalignment':0.9,
    'Contamination in lubricant':0.6,
    'Poor tensioning':0.8, 
    'Overheating':0.7,
    'Insulation breakdown':0.8,
    'Delayed maintenance':0.7,
    'Oil contamination':0.6,
    'Low suction pressure':0.7,
    'Blocked inlet':0.8,
    'Air ingress':0.6,
    'Oil leak':0.8,
    'Wrong lubricant grade':1.0,
    'Flow restriction':0.7, 
    'Valve malfunction':0.6,
    'Dirty filters':0.4
}

recommendation_weights={
    'No action needed':0.1,
    'Seal replacement and pressure test':0.9,
    'Electrical panel inspection and repair':0.8,
    'Valve replacement and flow test':0.7,
    'Cooling system flush and repair':0.6,
    'Bearing replacement and alignment check':1.0,
    'Belt replacement and tension adjustment':1.0,
    'Motor rewinding and electrical inspection':0.7,
    'Full lubrication system flush and refill':0.8,
    'Impeller replacement and inlet inspection':0.7,
    'Compressor stage inspection and filter replacement':0.7
}


def compute_mcdm_score(anomaly,failure_type,recommended_action,root_cause,severity):
    anomaly_binary=int(np.where(anomaly==-1,1,0))   
    severity_score=severity_weights.get(severity,0.0)
    recommendation_score=recommendation_weights.get(recommended_action,0.0)
    root_cause_score=root_cause_weights.get(root_cause,0.0)
    failure_score=failure_weights.get(failure_type,0.0)
    criteria=np.array((anomaly_binary,failure_score,recommendation_score,root_cause_score,severity_score))
    weights=np.array([0.1,0.4,0.1,0.2,0.2])
    mcdm_scores=np.dot(criteria,weights)
    return float(mcdm_scores)


# tuning  severity and anomaly

def tune_severity(row):
    if(row['anomaly']==0 and
    row['failure_type']=='No Failure' and
    row['root_cause']== 'No Fault Detected'):
        return"Low"
    else:
        return row['severity']

# building the MCDM engine and logic
def decision_engine(row):
    #severity tuning
    row['severity']=tune_severity(row)
    ## prediction based decisions
    if(
        row['anomaly']==0 and
        row['failure_type']=='No Failure' and 
        row['root_cause']=='No Fault Detected' and
        row['recommended_action']=='No action needed'):
        return 'Normal Operations'
        ## Severity Based Decisions
    mcdm_scores=row['mcdm_score']
    severity=row['severity']
    if row['anomaly']==1 and row['failure_type']=='No Failure':
        if severity== 'High':
            return "Urgent Inspection Required"
        if severity== 'Medium':
            return "Schedule Inspecton"
        if severity== 'Low':
            return "Monitor Closely"
        ## score based decisions
    if mcdm_scores>=0.7:
        return "Critical Fault: Initiate Corrective Maintenance"
    if mcdm_scores>=0.5:
        return "Fault Detected: Plan Maintenance Within 24 Hours"
    if mcdm_scores>=0.3:
        return "Minor Fault : Schedule Preventive Maintenance"
    else:
        return "Normal Operations"

