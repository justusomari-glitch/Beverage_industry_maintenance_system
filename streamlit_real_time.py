import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv
import mysql.connector


load_dotenv()

#Page Config
st.set_page_config(
    page_title="Real-Time Machine Monitoring",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card{
        background: linear-gradient(135deg, #1e2130, #252a3d);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #4CAF50;
        margin-bottom: 10px;
    }
    .metric-card.warning { border-left-color: #FF9800; 
    .metric-card.critical { border-left-color: #F44336; 
    .metric-card.normal { border-left-color: #4CAF50;}
    .section-header {
        font-size: 28px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 20px;
        color: #00d4ff;
        border-bottom: 2px solid #00d4ff;
        padding-bottom: 10px;
    }
    .kpi-value {font-size: 36px; font-weight: 800; color: #ffffff;}
    .kpi-label {font-size: 16px; color: #8899aa; text-transform: uppercase; letter-spacing: 1px;}
    .machine-card {
        background: #1a1f2e;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #2a3045;
    }
    .severity-high { color: #F44336; font-weight: bold; }
    .severity-medium { color: #FF9800; font-weight: bold; }
    .severity-low { color: #4CAF50; font-weight: bold; }
    .stSelectbox label { color: #00d4ff; !important; }
    </style>
""", unsafe_allow_html=True)

#DB Connection
def get_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        ssl_ca= os.getenv('SSL_CA_CERT'),
        ssl_verify_cert=True
    )
def get_data(table_name,limit=100):
    try:
        conn=get_connection()
        df=pd.read_sql(f"SELECT * FROM {table_name} ORDER BY created_at DESC LIMIT {limit}",conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        st.exception(e)
        return pd.DataFrame()
    
#TABLES mapping
SECTIONS= {
    "Packaging":"packaging_predictions",
    "Utilities":"utilities_predictions",
    "Production Line":"production_line_predictions",
    "Raw Material":"raw_material_predictions"
}
SENSOR_COLS=[
    "temperature","vibration","pressure","humidity","rotational_speed",
    "torque","current","voltage","flow_rate","oil_level","bearing_temperature",
    "product_temperature","noise_level","power_consumption",
]
#sidebar
st.sidebar.markdown("## ⚙️ Machine Monitoring Dashboard")
st.sidebar.markdown("___")
selected_section=st.sidebar.selectbox("Select Machine Section",list(SECTIONS.keys()))
refresh_rate=st.sidebar.slider("Refresh Rate (seconds)",5,60,15)
st.sidebar.markdown("___")
st.sidebar.markdown(f"last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

table=SECTIONS[selected_section]

#header
st.markdown(f"<h1 class='section-header'>{selected_section} Dashboard</h1>",unsafe_allow_html=True)
df=get_data(table,limit=300)
st.write(f"Rows fetched: {len(df)}, Columns: {len(df.columns)}")
st.write(df.head())
if df.empty:    
    st.warning("No data available for this section.Make sure the consumers pipeline is running and generating predictions.")
    st.stop()

#KPI Cards
total=len(df['machine_id'].unique())
anomalies= df[df['anomaly'] == 1].shape[0] if 'anomaly' in df.columns else 0
critical=len(df[df['severity'] == "High"]) if 'severity' in df.columns else 0
avg_mcdm=round(pd.to_numeric(df['mcdm_score'],errors='coerce').mean(),2) if 'mcdm_score' in df.columns else 0

col1,col2,col3,col4=st.columns(4)
with col1:
    st.markdown(f"""
    <div class='metric-card normal'>
        <div class='kpi-value'>{total}</div>
        <div class='kpi-label'>Total Machines</div>
        </div>""",unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class='metric-card warning'>
        <div class='kpi-value'>{anomalies}</div>
        <div class='kpi-label'>Anomalies Detected</div>
        </div>""",unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class='metric-card critical'>
        <div class='kpi-value'>{critical}</div>
        <div class='kpi-label'>Critical Issues</div>
        </div>""",unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class='metric-card normal'>
        <div class='kpi-value'>{avg_mcdm}</div>
        <div class='kpi-label'>Average MCDM Score</div>
        </div>""",unsafe_allow_html=True)
    
st.markdown("___")
#Latest Predictions per machine
st.markdown("### Machine Status")
latest=df.sort_values("created_at").groupby("machine_id").last().reset_index()

cols= st.columns(3)
for i,(_,row) in enumerate(latest.iterrows()):
    severity=row.get("severity","Unknown")
    severity_class= "severity-high" if severity=="High" else "severity-medium" if severity=="Medium" else "severity-low"
    with cols[i%3]:
        st.markdown(f"""
        <div class='machine-card'>
            <b>{row.get("machine_name","Unknown")}</b><br>
            <small>Type: {row.get("machine_type","-")}</small><br><br>
            Anomaly: <b>{row.get("anomaly","-")}</b><br>
            Failure: <b>{row.get("failure_type","-")}</b><br>
            Severity: <span class='{severity_class}'>{severity}</span><br>
            Recommended Action: <b>{row.get("recommended_action","-")}</b><br>
            Priority: <b>{row.get("priority","-")}</b><br>
            MCDM Score: <b>{row.get("mcdm_score","-")}</b>
        </div>
        <hr style="border:1px solid #2a3045;margin:10px 0;">
        """,unsafe_allow_html=True)
st.markdown("___")
#Sensor Trends
st.markdown("### Sensor Trends")
available_sensors=[s for s in SENSOR_COLS if s in df.columns]
selected_sensors=st.multiselect("Select Sensors to Plot",available_sensors,default=available_sensors[:4])

if selected_sensors:
    df_sorted=df.sort_values("created_at")
    fig=go.Figure()
    for sensor in selected_sensors:
        fig.add_trace(go.Scatter(
            x=df_sorted["created_at"],
            y=df_sorted[sensor],
            mode="lines",
            name=sensor.replace("_"," ").title()
        ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        height=400,
        margin=dict(l=0,r=0,t=30,b=0)
    )
    st.plotly_chart(fig,use_container_width=True)

#severity distribution
col1,col2=st.columns(2)
with col1:
    st.markdown("### Severity Distribution")
    if 'severity' in df.columns:
        severity_counts=df['severity'].value_counts().reset_index()
        severity_counts.columns=['severity','count']
        fig2=px.pie(
            severity_counts,
            names='severity',
            values='count',
            color_discrete_map={"High":"#F44336","Medium":"#FF9800","Low":"#4CAF50"},
                   template="plotly_dark")
        fig2.update_layout(
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
        )
        st.plotly_chart(fig2,use_container_width=True)
with col2:
    st.markdown("### Failure Type Distribution")
    if 'failure_type' in df.columns:
        failure_counts=df['failure_type'].value_counts().reset_index()
        failure_counts.columns=['failure_type','count']
        fig3=px.bar(failure_counts,x='count',y='failure_type',orientation='h',
                   color='failure_type',template="plotly_dark",
                   color_discrete_sequence=['#00d4ff'])
        fig3.update_layout(
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            height=350
        )
        st.plotly_chart(fig3,use_container_width=True)
#llm explanations
st.markdown("___")
st.markdown("### LLM-Generated Maintenance Recommendations")
latest=(
    df.sort_values("created_at")
    .iloc[[-1]]
    .reset_index(drop=True)
)
row=latest.iloc[0]
machine_name=row.get("machine_name","Unknown")
if pd.notna(row.get("system_explanations")) or pd.notna(row.get("system_recommendations")):
    st.markdown(f"#### {machine_name}")
    if pd.notna(row.get("system_explanations")):
        st.info(row["system_explanations"])
    if pd.notna(row.get("system_recommendations")):
        st.success(row["system_recommendations"])
    st.markdown("---")

time.sleep(refresh_rate)
st.rerun()

       
 