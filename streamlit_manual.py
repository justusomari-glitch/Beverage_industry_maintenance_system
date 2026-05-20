import streamlit as st
import requests
import json
import plotly.graph_objects as go

#-- page config
st.set_page_config(
    page_title="Maintenance System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL=st.secrets["API_URL"]
st.markdown("""
<style>
.stApp{
    background-color: #000000 !important;
}
[data-testid="stSidebar"]{
    background-color: #000000 !important;
}

/* Specific Overides For each card type */
.result-card.anomaly .value,
.result-card.ok .value,
.result-card.info .value,
.result-card.warn .value,
.result-card.danger .value,
.result-card.success .value,
.result-card.accent .value {
    color: white !important;
}
</style>
""",unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700&display=swap');
/* Root palette */
:root {
    --bg:      #0a0e1a;
    --panel:    #111827;
    --border:   #1e3a5f;
    --accent:   #00d4ff;
    --accent2:  #ff6b35;
    --success:  #00ff88;
    --danger:   #ff3d71;
    --warn:     #ffaa00;
    --text:     #e2e8f0;
    --muted:    #64748b;
    --mono:     'Share Tech Mono',monospace;
    --body:     'Exo 2',sans-serif;
}
html,body,[class*="css"] {
    background-color: var(--bg) !important;
    colour: var(--text) !important;
    font-family: var(--body) !important;
}
/*Hide Streamlit Chrome */
#MainMenu, footer, header {visibility: hidden;}
/* --Header banner --*/
.bims-header{
    background: linear-gradient(135deg, #0a0e1a 0%, #0f2040 50%, #0a0e1a 100%);
    boarder: 1px solid var(--boarder);
    boarder-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.bims-header::before{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
}
.bims-header h1{
    front-family: var(--mono) !important;
    font-size: 1.6rem !important;
    color: var(--accent) !important;
    letter-spacing: 3px;
    margin: 0 !important;
    text-shadow: 0 0 20px rgba(0,212,255,0.4);
}
.bims-header p {
    colour: var(--muted);
    margin: 6px 0 0 0;
    font-size: 0.85rem;
    letter-spacing: 1px;
}
/* -- Section Labels -- */
.section-label {
    font-family: var(--mono);
    font-size: 0.7rem;
    letter-spacing: 4px;
    color: var(--accent);
    text-transform: uppercase;
    border-left: 3px solid var(--accent);
    padding-left: 10px;
    margin: 24px 0 14px 0;
}
/* -- Result cards -- */
.result-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 14px;
    psition: relative;
}
.result-card::before{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 10px 0 0 10px;
    }
.result-card.anomaly::before {background: var(--danger);}
.result-card.ok::before {background: var(--success);}
.result-card.info::before {background: var(--accent);}
.result-card.warn::before {background: var(--warn);}

.result.card .label{
    ffont-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 6px
}
.result-card .value {
    font-size: 1.3rem;
    font-weight: 700;
    colour: var(--text)
}
.result-card .value.danger {colour: var(--danger);}
.result-card .value.success {colour: var(--success);}
.result-card .value.warn {colour: var(--warn);}
.result-card .value.accent {colour: var(--accent);}

/* -- MCDM Score Bar -- */
.score-bar-wrap {margin-top: 10px;}
.score-bar-bg {
    background: #1a2744;
    border-radius: 4px;
    height: 10px;
    overflow: hidden;
}
.score-bar-fill {
    height: 10px;
    border-radius: 4px;
    transisition; width 0.8s ease}
            
/* -- SHAP TABLES -- */
.shap-table {
    width: 100%;
    border-collapse: collapse;
    font-family: var(--mono);
    font-size: 0.8rem;
}
.shap-table th {
    colour: var(--muted);
    font-weight: 400;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-size: 0.65rem;
    padding: 8x 12px;
    border-bottom: 1px solid var(--border);
    text-align: left;
}
.shap-table td {
    padding: 8px 12px;
    border-bottom: 1px solid #1a2744;
    color: var(--text);
}
.shap-pos {color: var(--danger);}
.shap-neg {color: var(--success);}
            
/* -- LLM EXPLANATION -- */
.llm-box {
    background: #0d1b2e;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px 22px;
    font-size: 0.88rem;
    line-height: 1.7;
    color: #94a3b8;
    white-space: pre-wrap;
}
/* -- Streamlit Widget Overides -- */
.stSlider > div > div > div {background: var(--accent) !important;}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 6px!important;
}
.stButton > button {
    background: linear-gradient(135deg, #005f8a, #00d4ff) !important;
    color: #000 !important;
    font-family: var(--mono) !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 10px 32px !important;
    width: 100%;
    font-size: 0.9rem !important;
    text-transform: uppercase;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #007ab5, #33ddff) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(0,212,255,0.3)
}
label, .stMarkdown p {color: var(--text) !important; }
.sidebar .sidebar-content {color: var(--panel) !important; }
</style>
""", unsafe_allow_html=True)

# header
st.markdown("""
<div class="bims-header">
    <h1> MAINTENANCE SYSTEM </h1>
    <p>PREDICTIVE MAINTENANCE . ANOMALY DETECTION . FAILURE ANALYSIS</p>
</div>
""",unsafe_allow_html=True)

# sidebar inputs
with st.sidebar:
    st.markdown('<div class="selection-label">Sensor Input Parameters</div>',unsafe_allow_html=True)
    temperature= st.number_input("Temperature (C)", value=91.0, step=0.1)
    vibration= st.number_input("Vibration (mm/s)", value=2.5, step=0.01)
    pressure= st.number_input("Pressure (bar)", value=10.5, step=0.1)
    rotation_speed= st.number_input("Rotation Speed (RPM)", value=1517.0, step=1.0)
    torque= st.number_input("Torque (N-m)", value=17.0, step=0.1)
    voltage= st.number_input("Voltage (V)", value=340.0, step=0.1)
    current= st.number_input("Current (A)", value=32.0, step=0.1)
    power_consumption= st.number_input("Power Consumption (kW)", value=23.2, step=0.01)
    humidity= st.number_input("Humidity (%)", value=65.0, step=0.1)
    noise_level= st.number_input("Noise Level (dB)", value=68.0, step=0.1)
    flow_rate= st.number_input("Flow Rate (L/min)", value=400.0, step=0.1)
    product_temperature= st.number_input("Product Temperature (C)", value=84.0, step=0.1)
    oil_level= st.number_input("Oil Level (%)", value=78.0, step=0.1)
    bearing_temperature= st.number_input("Bearing Temperature (C)", value=45.0, step=0.1)

    st.markdown('<div class="selection-label">Operational Parameters</div>',unsafe_allow_html=True)
    cleaning_cycle_status= st.selectbox("Cleaning Cycle Status",[1,0], format_func=lambda x: "Active" if x else "Inactive")
    hours_since_maintenance= st.number_input("Hours Since Maintenance (C)", value=5, step=1,min_value=0)
    zone= st.selectbox("Zone",["Zone B","Zone C","Zone D","Zone A"])
    criticality_level= st.selectbox("Criticality Level",["Low","Medium","High"])

    st.markdown("---")
    run_predict=st.button("RUN PREDICTION")


# main panel
if run_predict:
    payload={
        "temperature": temperature,
        "vibration": vibration,
        "pressure": pressure,
        "rotation_speed": rotation_speed,
        "torque": torque,
        "voltage": voltage,
        "current": current,
        "power_consumption": power_consumption,
        "humidity": humidity,
        "noise_level": noise_level,
        "flow_rate": flow_rate,
        "product_temperature": product_temperature,
        "cleaning_cycle_status": cleaning_cycle_status,
        "oil_level": oil_level,
        "bearing_temperature": bearing_temperature,
        "hours_since_maintenance": hours_since_maintenance,
        "zone": zone,
        "criticality_level": criticality_level
    }

    with st.spinner("Annalysing Sensor Data..."):
        try:
            resp= requests.post(f"{API_URL}/predict",json=payload,timeout=60)
            resp.raise_for_status()
            result=resp.json()
            st.session_state.result=result
        except requests.exceptions.ConnectionError:
            st.error("Cannot Reach FASTAPI")
            st.stop()
        except Exception as e:
            st.error(f"Request failed: {e}")
            st.stop()

    st.markdown('<div class="selection-label">Prediction Results</div>',unsafe_allow_html=True)
    anomaly =result.get("anomaly",0)
    failure_type =result.get("failure_type","N/A")
    severity =result.get("severity","N/A")
    priority =result.get("priority","N/A")
    mcdm_score =result.get("mcdm_score",0)
    rec_action =result.get("recommended_action","N/A")
    root_cause =result.get("root_cause","N/A")

    col1,col2,col3,col4=st.columns(4)
    with col1:
        card_cls="anomaly" if anomaly else "ok"
        val_cls= "danger" if anomaly else "success"
        val_txt= "ANOMALY DETECTED" if anomaly else "NORMAL"
        st.markdown(f"""
        <div class="result-card {card_cls}">
            <div class="label">System Status</div>
            <div class="value {val_cls}">{val_txt}</div>
        </div>""",unsafe_allow_html=True
        )
    with col2:
        st.markdown(f"""
        <div class="result-card info">
            <div class="label">Failure Type</div>
            <div class="value accent">{failure_type}</div>
        </div>""",unsafe_allow_html=True
        )

    with col3:
        sev_cels= "danger" if severity in ['High'] else 'warn'if severity =='Medium' else "success"
        st.markdown(f"""
        <div class="result-card warn">
            <div class="label">Severity</div>
            <div class="value {sev_cels}">{severity}</div>
        </div>""",unsafe_allow_html=True)
    with col4:
        score_pct=min(max(float(mcdm_score)*100,0),100)
        bar_colour= "#ff3d71" if score_pct > 70 else "#ffaa00" if score_pct>40 else "#00ff88"
        st.markdown(f"""
        <div class="result-card info">
            <div class="label">MCDM risk score</div>
            <div class="value">{mcdm_score:.2f}</div>
            <div class="score-bar-wrap">
                <div class="score-bar-bg">
                    <div class="score-bar-fill"style="width":{score_pct}%;background;"></div>
                </div>
            </div>
        </div>""",unsafe_allow_html=True)


    col5,col6=st.columns(2)
    with col5:
        st.markdown(f"""
        <div class="result-card warn">
            <div class="label">Recommended Action</div>
            <div class="value" style="font-size:1rem;">{rec_action}</div>
        </div>""",unsafe_allow_html=True
        )
    
    with col6:
        st.markdown(f"""
        <div class="result-card info">
            <div class="label">Root Cause</div>
            <div class="value" style="font-size:1rem;">{root_cause}</div>
        </div>""",unsafe_allow_html=True
        )
    st.markdown(f"""
    <div class="result-card info" style="margin-top:10px;">
        <div class="label">Priority and Decisions</div>
        <div class="value">{priority}</div>
    </div>""",unsafe_allow_html=True)

    #shap explainability
    explanations=result.get("explanations",{})
    anomaly_shap=explanations.get("anomaly_explanation",{})
    failure_shap=explanations.get("failure_type_explanation",{})

    if anomaly_shap or failure_shap:
        st.markdown('<div class="selection-label">SHAP feature Importance</div>',unsafe_allow_html=True)
        shap_col1,shap_col2=st.columns(2)

        def render_shap_chart(shap_dict,title):
            if not shap_dict:
                st.markdownst("<p style='colour:#64748b;font-size:0.8rem;'>No SHAP data available.</p>",unsafe_allow_html=True)
                return
            
            sorted_items= sorted(shap_dict.items(),key=lambda x: abs(float(x[1])),reverse=True)[:10]
            sorted_items=sorted(sorted_items,key=lambda x: float(x[1]))

            features= [item[0].replace("_","").title() for item in sorted_items]
            values=[float(item[1]) for item in sorted_items]
            colors=["#ff3d71" if v>0 else "#00ff88" for v in values]
            labels= [f"{v:+.4f}" for v in values]

            fig= go.Figure(go.Bar(
                x=values,
                y=features,
                orientation="h",
                marker_color=colors,
                text=labels,
                textposition="outside",
                textfont=dict(color="#e2e8f0",size=10,family="monospace"),
                hovertemplate="<b>%{y}</b><br>SHAP: %{x:+.4f}<extra></extra>",
            ))

            fig.add_vline(x=0, line_color="#00d4ff",line_width=1.5)

            fig.update_layout(
                title= dict(text=title,font=dict(color="#00d4ff",size=11,family="monospace"),x=0),
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                font=dict(color="#e2e8f0",family="monospace"),
                xaxis=dict(
                    title="SHAP Value",
                    color="#64748b",
                    gridcolor="#1e3a5f",
                    zerolinecolor="#1e3a5f",
                ),
                yaxis=dict(color="#e2e8f0",gridcolor="#1a2744"),
                margin=dict(l=10, r=80, t=40, b=30),
                height=max(300,len(features)* 36),
                showlegend=False,
            )
            st.plotly_chart(fig,use_container_width=True)
        with shap_col1:
            st.markdown('<p style="font-family:monospace;font-size:0.7rem;color:#00d4ff;letter-spacing:3px;margin-bottom:4px;">ANOMALY MODEL</p>',unsafe_allow_html=True)
            render_shap_chart(anomaly_shap,"Anomaly Detection-Feature Impact")
        with shap_col2:
            st.markdown('<p style="font-family:monospace;font-size:0.7rem;color:#00d4ff;letter-spacing:3px;margin-bottom:4px;">FAILURE TYPE MODEL</p>',unsafe_allow_html=True)    
            render_shap_chart(failure_shap,"Failure Classification-Feature Impact")

    #llm_explanarion
    llm_explanation =result.get("system_explanations","")
    llm_recommandation=result.get("system_recommendations","")

    if llm_explanation or llm_recommandation:
        st.markdown('<div class="section-label">AI System Analysis</div>',unsafe_allow_html=True)
        llm_c1,llm_c2=st.columns(2)

        with llm_c1:
            st.markdown("**System Explanation**")
            st.markdown(f'<div class="llm-box">{llm_explanation or "N/A"}</div>',unsafe_allow_html=True)
        with llm_c1:
            st.markdown("**System Recommendation**")
            st.markdown(f'<div class="llm-box">{llm_recommandation or "N/A"}</div>',unsafe_allow_html=True)
        
    with st.expander("Raw API RESPONSE"):
        st.json(result)



    #chatbot intergration
    
else:
    st.markdown("""
    <div style="
        text-align:center;
        padding: 80px 20px;
        color: #1e3a5f;
        font-family: 'Share Tech Mono',monospace;
        font-size: 0.9rem;
        letter-spacing: 3px;
    ">
        <div style= "font-size:3rem;margin-bottom:16px;"></div>
        CONFIGURE SENSOR PARAMETERS IN THE SIDEBAR<br>
        THEN CLICK <span style="color:#00d4ff;">RUN PREDICTION</span>
    </div>
    """,unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="section-lebel">Chat With AI Assistant</div>',unsafe_allow_html=True)
if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]
for msg in st.session_state.chat_history:
    role_color= "#00d4ff" if msg["role"] == "assistant" else "#e2e8f0"
    role_label= "AI" if msg["role"]== "assistant" else "You"
    st.markdown(f"""
    <div style="margin-bottom:12px;">
        <span style="font-family:monospace;font-size:0.7rem;color:{role_color};letter-spacing:2px;">{role_label}</span>
        <div class="llm-box" style="margin-top:4px;">{msg["content"]}</div>
    </div>""",unsafe_allow_html=True)
user_input=st.text_input("Ask About This Prediction....",key="chat_input",
                             placeholder="e.g Why is this Motor Failing?")
col1,col2=st.columns(2)
with col1:
    if st.button("Send",key="chat_send") and user_input.strip():
        st.session_state.chat_history.append({"role":"user","content":user_input})
        try:
            chat_resp=requests.post(f"{API_URL}/chat",json={
                "user_message":user_input,
                "conversation_history":st.session_state.chat_history[:-1],
                "prediction_context":{}
            },timeout=60)
            chat_resp.raise_for_status()
            ai_reply=chat_resp.json().get("response","No Response.")
        except Exception as e:
            ai_reply=f"Error:{e}"
        st.session_state.chat_history.append({"role":"assistant","content":ai_reply})
        st.rerun()
with col2:
    if st.button("Clear Chat", key="clear_chat"):
        st.session_state.chat_history=[]
        st.rerun()

            



    




          


        
            
            
            
            
            
            
            
            
            
            
            