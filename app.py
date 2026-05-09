import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings

# Suppress the deprecation warnings so your terminal stays clean
warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- 1. SETTINGS ---
st.set_page_config(page_title="OMNI Balkan Hub", layout="wide", page_icon="🚛")

# --- 2. DATA INITIALIZATION ---
if 'fleet_data' not in st.session_state:
    st.session_state.fleet_data = pd.DataFrame([
        {'Truck_ID': 'PR-102-AL', 'Driver': 'Dragan P.', 'City': 'Pristina', 'lat': 42.66, 'lon': 21.16, 'Status': 'Active', 'Fuel': 85, 'Route': 'Prishtina -> Belgrade', 'ETD': '14:00', 'Actual': '13:55'},
        {'Truck_ID': 'BG-550-TX', 'Driver': 'Amar H.', 'City': 'Belgrade', 'lat': 44.78, 'lon': 20.44, 'Status': 'Active', 'Fuel': 42, 'Route': 'Belgrade -> Skopje', 'ETD': '18:30', 'Actual': '18:45'},
        {'Truck_ID': 'ZG-991-HR', 'Driver': 'Luka V.', 'City': 'Zagreb', 'lat': 45.81, 'lon': 15.98, 'Status': 'Maintenance', 'Fuel': 91, 'Route': 'Zagreb -> Sarajevo', 'ETD': '12:00', 'Actual': '12:05'},
        {'Truck_ID': 'SJ-442-BA', 'Driver': 'Edin D.', 'City': 'Sarajevo', 'lat': 43.85, 'lon': 18.41, 'Status': 'Active', 'Fuel': 12, 'Route': 'Sarajevo -> Tirana', 'ETD': '09:00', 'Actual': '09:30'},
        {'Truck_ID': 'SK-110-MK', 'Driver': 'Bekim S.', 'City': 'Skopje', 'lat': 41.99, 'lon': 21.42, 'Status': 'Active', 'Fuel': 77, 'Route': 'Skopje -> Prishtina', 'ETD': '11:00', 'Actual': '10:50'}
    ])

# --- 3. STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc !important; }
    h1, h2, h3, h4, p, label, [data-testid="stMetricValue"] { color: #0f172a !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e2e8f0; }
    [data-testid="stSidebar"] * { color: #1e293b !important; }
    .stButton>button { background-color: #f97316 !important; color: white !important; width: 100%; border: none; font-weight: bold; height: 3em; }
    .audit-box { background-color: #0f172a; color: #22c55e; padding: 15px; border-radius: 8px; font-family: monospace; border-left: 5px solid #f97316; margin-bottom: 10px; line-height: 1.5; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color: #f97316;'>OMNI</h1>", unsafe_allow_html=True)
    page = st.radio("MENU", ["Dashboard", "Drivers", "Fleet Registry", "Audits", "Analytics"])

# --- 5. DASHBOARD ---
if page == "Dashboard":
    st.header("Operations Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Active Fleet", len(st.session_state.fleet_data))
    c2.metric("Efficiency", "92%")
    c3.metric("Alerts", "1 Low Fuel")

    st.subheader("Live Fleet Location")
    # Switched back to scatter_mapbox to ensure the map actually renders
    fig = px.scatter_mapbox(
        st.session_state.fleet_data, lat="lat", lon="lon", 
        hover_name="Truck_ID", hover_data=["Driver", "Status"],
        zoom=5, height=600
    )
    # The Circles
    fig.update_traces(marker=dict(size=25, color="#f97316", opacity=0.9)) 
    # The Map Style (Carto-positron is free and high contrast)
    fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

# --- 6. DRIVERS & FLEET ---
elif page in ["Drivers", "Fleet Registry"]:
    st.header(f"{page} Management")
    
    with st.expander(f"Add New Entry"):
        with st.form("add_form"):
            new_id = st.text_input("ID / Plate")
            new_name = st.text_input("Name")
            new_city = st.selectbox("Hub", ["Pristina", "Belgrade", "Skopje", "Tirana", "Sarajevo"])
            if st.form_submit_button("Submit"):
                if new_id and new_name:
                    coords = {"Pristina": (42.66, 21.16), "Belgrade": (44.78, 20.44), "Skopje": (41.99, 21.42), "Tirana": (41.32, 19.81), "Sarajevo": (43.85, 18.41)}
                    lat, lon = coords[new_city]
                    new_row = pd.DataFrame([{'Truck_ID': new_id, 'Driver': new_name, 'City': new_city, 'lat': lat, 'lon': lon, 'Status': 'Active', 'Fuel': 100, 'Route': 'Unassigned', 'ETD': '00:00', 'Actual': '00:00'}])
                    st.session_state.fleet_data = pd.concat([st.session_state.fleet_data, new_row], ignore_index=True)
                    st.rerun()
    
    st.dataframe(st.session_state.fleet_data, use_container_width=True, hide_index=True)

# --- 7. AUDITS (BLACK BOX) ---
elif page == "Audits":
    st.header("Operational Black Box")
    for _, row in st.session_state.fleet_data.iterrows():
        status = "ON TIME" if row['Actual'] <= row['ETD'] else "DELAYED"
        color = "#22c55e" if status == "ON TIME" else "#ef4444"
        st.markdown(f"""
            <div class="audit-box">
                [SYSTEM LOG]: {row['Truck_ID']} | DRIVER: {row['Driver']} <br>
                ROUTE: {row['Route']} <br>
                EXPECTED: {row['ETD']} | ARRIVAL: {row['Actual']} <br>
                STATUS: <span style="color: {color};">{status}</span>
            </div>
        """, unsafe_allow_html=True)

# --- 8. ANALYTICS ---
elif page == "Analytics":
    st.header("Advanced Analytics")
    r1c1, r1c2, r1c3 = st.columns(3)
    
    # 1. Fuel Gauge
    fig1 = go.Figure(go.Indicator(mode="gauge+number", value=st.session_state.fleet_data['Fuel'].mean(), title={'text': "Fleet Fuel"}, gauge={'bar': {'color': "#f97316"}}))
    r1c1.plotly_chart(fig1, use_container_width=True)
    
    # 2. Composition
    fig2 = px.pie(st.session_state.fleet_data, names='Status', color_discrete_sequence=['#f97316', '#0f172a'])
    r1c2.plotly_chart(fig2, use_container_width=True)
    
    # 3. Hub Bar Chart (Plotly version so it doesn't crash)
    fig3 = px.bar(st.session_state.fleet_data, x='City', title="Hub Distribution", color_discrete_sequence=['#f97316'])
    r1c3.plotly_chart(fig3, use_container_width=True)

    r2c1, r2c2, r2c3 = st.columns(3)
    # 4. Delays
    delays = len(st.session_state.fleet_data[st.session_state.fleet_data['Actual'] > st.session_state.fleet_data['ETD']])
    r2c1.metric("Delayed Arrivals", delays)
    # 5. Maintenance
    maint = len(st.session_state.fleet_data[st.session_state.fleet_data['Status'] == 'Maintenance'])
    r2c2.metric("Maintenance", maint)
    # 6. Regions
    r2c3.metric("Regions", len(st.session_state.fleet_data['City'].unique()))