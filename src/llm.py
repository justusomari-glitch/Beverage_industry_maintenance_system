import os
from groq import Groq

GROQ_MODEL="llama-3.1-8b-Instant"

def init_groq_client():
    return Groq(api_key=os.getenv('GROQ_API_KEY'))


# llm for explanation

def get_llm_explanation(groq_client,anomaly_binary,failure_type,recommended_action,
        root_cause,tuned_severity,scores,anomaly_shap,failure_type_shap):
    """
    LLM USE 1-EXPLAINABILITY
    Explains what is happening to the machine in human readable format
    """
    prompt= f"""
    You are an Industry Machine Maintenance expert system.
    A machine sensor analysis has produced the following results:
    -Anomaly : {anomaly_binary}
    -Failure type: {failure_type}
    -Recommended Action: {recommended_action}
    -Root cause: {root_cause}
    -Severity: {tuned_severity}
    -MCDM Score: {scores}

    Top Contributing sensor features from shap analysis
    -Anomaly SHAP:{anomaly_shap}
    -Failure SHAP:{failure_type_shap}
    
    Provide a clear and concise explanation :
    1. What is happening with this machine
    2. Why these sensor readings are concerning 
    3.The urgency of the situation

    Keep it technical but understandable for a maintenance operator.
    Max 4 sentences
    """
    response=groq_client.chat.completions.create(
        model= GROQ_MODEL,
        messages=[
            {
                "role":"system",
                "content":"You are an expert in industry machine maintenance and failure analysis"
            },
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0.3,
        max_tokens=300
    )
    return response.choices[0].message.content

def get_llm_recommendation(groq_client,anomaly_binary,failure_type,recommended_action,
        root_cause,tuned_severity,scores,anomaly_shap,failure_type_shap):
    """
    LLM USE 2-DYNAMIC RECOMMENDATIONS
    Generates dynamic maintenance recommendations beyond rule-based engine
    """
    prompt=f"""
    You are an Industry Machine Maintenance expert system.
    Based on this machine failure analysis:
    -Anomaly : {anomaly_binary}
    -Failure type: {failure_type}
    -Recommended Action: {recommended_action}
    -Root cause: {root_cause}
    -Severity: {tuned_severity}
    -MCDM Score: {scores}

    Top Contributing sensor features from shap analysis
    -Anomaly SHAP:{anomaly_shap}
    -Failure SHAP:{failure_type_shap}

    Provide exactly 3 specific,actionable maintenance recommendations:
    1. Immediate action(what to do now)
    2. Short term action (within 24 hours)
    3. Preventive action (to avoid recurrence)

    Be concise and technical
    """
    response=groq_client.chat.completions.create(
        model= GROQ_MODEL,
        messages=[ { "role":"system","content":"You are an expert in industry machine maintenance and failure analysis"},
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0.3,
        max_tokens=300
    )
    return response.choices[0].message.content


def get_llm_chat_response(groq_client,user_message,conversation_history,anomaly_binary,failure_type,recommended_action,
        root_cause,tuned_severity,scores,priority):
    """
    LLM USE 3-CONVENTIONAL INTERFACE
    Allows the operator to chat with the system on the predictions
    """
    system_prompt= f"""
    You are an industry maintenace AI assistant.
    You have acces to the following current machine prediction context:
    -Anomaly : {anomaly_binary}
    -Failure type: {failure_type}
    -Recommended Action: {recommended_action}
    -Root cause: {root_cause}
    -Severity: {tuned_severity}
    -MCDM Score: {scores}
    -Priority :{priority}

    Answer the machine operator based on this context.
    Be concise ,technical and focus on industry machine
    If asked something outside this context say you only have acces to the current machine prediction data.
    """
    messages=[{"role":"system","content":system_prompt}]

    for turn in conversation_history:
        messages.append({
            "role":turn["role"],
            "content":turn["content"]
        })
    messages.append({"role":"user","content":user_message})

    response=groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.5,
        max_tokens=300
    )
    return response.choices[0].message.content


