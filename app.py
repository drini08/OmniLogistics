import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
import random
import threading
import time
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="OMNI Balkan Hub",
    layout="wide",
    page_icon="🚛",
    initial_sidebar_state="expanded"
)

# Auto-refresh to update live simulation data every 5 seconds


st.markdown("""
<style>
/* MINIMALIST DARK THEME */

:root {
    --bg-dark: #0a0a0a;
    --bg-secondary: #121212;
    --bg-tertiary: #1a1a1a;
    --text-primary: #ededed;
    --text-secondary: #a1a1aa;
    --text-tertiary: #71717a;
    --accent: #ffffff;
    --accent-light: #e5e5e5;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --border: #27272a;
}

* {
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background-color: var(--bg-dark) !important;
}

html, body {
    background-color: var(--bg-dark) !important;
}

[data-testid="stAppViewContainer"] {
    background-color: var(--bg-dark) !important;
}

[data-testid="stHeader"] {
    background-color: var(--bg-dark) !important;
    border-bottom: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    padding: 24px 16px !important;
}

.stTabs [data-baseweb="tab-list"] {
    background-color: transparent !important;
    border-bottom: 1px solid var(--border) !important;
}

.stTabs [aria-selected="true"] {
    border-bottom: 2px solid var(--text-primary) !important;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    letter-spacing: -0.02em !important;
}

p, label, span {
    color: var(--text-secondary) !important;
}

.stButton>button {
    background: transparent !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    font-weight: 500 !important;
    height: 3em !important;
    transition: all 0.2s ease !important;
    border-radius: 6px !important;
}

.stButton>button:hover {
    background: var(--bg-tertiary) !important;
    border-color: var(--text-secondary) !important;
}

/* METRIC CARDS */
[data-testid="stMetric"], .metric-card {
    background-color: var(--bg-dark) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 16px !important;
    box-shadow: none !important;
}

[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    font-size: 1.8rem !important;
    letter-spacing: -0.02em !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

.metric-card strong {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

.metric-card p {
    color: var(--text-secondary) !important;
}

/* STATUS STYLES */
.status-active {
    color: var(--success) !important;
    font-weight: 500 !important;
}

.status-maintenance {
    color: var(--warning) !important;
    font-weight: 500 !important;
}

.status-inactive {
    color: var(--danger) !important;
    font-weight: 500 !important;
}

/* AUDIT BOX */
.audit-box {
    background-color: var(--bg-secondary) !important;
    color: var(--text-secondary) !important;
    padding: 16px !important;
    border-radius: 6px !important;
    font-family: 'Courier New', monospace !important;
    border: 1px solid var(--border) !important;
    margin-bottom: 12px !important;
    line-height: 1.5 !important;
}

/* INPUT FIELDS */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input {
    background-color: var(--bg-dark) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 6px !important;
    padding: 10px 12px !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stDateInput"] input:focus {
    border-color: var(--text-secondary) !important;
    box-shadow: none !important;
}

/* SELECTBOX */
[data-testid="stSelectbox"] > div {
    background-color: var(--bg-dark) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    background-color: var(--bg-dark) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

[data-testid="stDataFrame"] table {
    background-color: var(--bg-dark) !important;
}

[data-testid="stDataFrame"] thead {
    background-color: var(--bg-secondary) !important;
}

[data-testid="stDataFrame"] thead th {
    color: var(--text-secondary) !important;
    border-bottom: 1px solid var(--border) !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em !important;
}

[data-testid="stDataFrame"] tbody td {
    color: var(--text-primary) !important;
    border-bottom: 1px solid var(--border) !important;
    font-size: 0.9rem !important;
}

[data-testid="stDataFrame"] tbody tr:hover {
    background-color: var(--bg-secondary) !important;
}

/* PROGRESS BAR */
.stProgress > div > div {
    background-color: var(--text-primary) !important;
}

/* DIVIDER */
.stDivider {
    border-color: var(--border) !important;
}

/* RADIO BUTTONS */
[data-testid="stRadio"] > div {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stRadio"] label {
    color: var(--text-secondary) !important;
    margin-bottom: 6px !important;
    font-weight: 500 !important;
}

/* EXPANDER */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    background-color: var(--bg-dark) !important;
    border-radius: 8px !important;
}

/* INFO/WARNING/ERROR BOXES */
.stInfo {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 6px !important;
}

.stWarning {
    background-color: rgba(245, 158, 11, 0.1) !important;
    border: 1px solid rgba(245, 158, 11, 0.2) !important;
    color: var(--warning) !important;
    border-radius: 6px !important;
}

.stError {
    background-color: rgba(239, 68, 68, 0.1) !important;
    border: 1px solid rgba(239, 68, 68, 0.2) !important;
    color: var(--danger) !important;
    border-radius: 6px !important;
}

.stSuccess {
    background-color: rgba(16, 185, 129, 0.1) !important;
    border: 1px solid rgba(16, 185, 129, 0.2) !important;
    color: var(--success) !important;
    border-radius: 6px !important;
}

/* BADGES */
.badge {
    display: inline-block !important;
    padding: 4px 8px !important;
    border-radius: 4px !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-right: 8px !important;
    border: 1px solid transparent !important;
}
.badge-green {
    background-color: rgba(16, 185, 129, 0.1) !important;
    color: var(--success) !important;
    border-color: rgba(16, 185, 129, 0.2) !important;
}
.badge-orange {
    background-color: rgba(245, 158, 11, 0.1) !important;
    color: var(--warning) !important;
    border-color: rgba(245, 158, 11, 0.2) !important;
}
.badge-blue {
    background-color: rgba(96, 165, 250, 0.1) !important;
    color: #60a5fa !important;
    border-color: rgba(96, 165, 250, 0.2) !important;
}
.badge-red {
    background-color: rgba(239, 68, 68, 0.1) !important;
    color: var(--danger) !important;
    border-color: rgba(239, 68, 68, 0.2) !important;
}
.badge-gray {
    background-color: rgba(113, 113, 122, 0.1) !important;
    color: var(--text-tertiary) !important;
    border-color: rgba(113, 113, 122, 0.2) !important;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: var(--bg-dark);
}

::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-tertiary);
}

</style>
""", unsafe_allow_html=True)

BALKAN_CITIES = {
    'Pristina': (42.66, 21.16),
    'Belgrade': (44.78, 20.44),
    'Skopje': (41.99, 21.42),
    'Tirana': (41.32, 19.81),
    'Sarajevo': (43.85, 18.41),
    'Zagreb': (45.81, 15.98),
    'Split': (43.51, 16.44),
    'Niš': (43.32, 21.89),
    'Podgorica': (42.43, 19.26),
    'Ljubljana': (46.06, 14.51)
}

if 'drivers_data' not in st.session_state:
    st.session_state.drivers_data = pd.DataFrame([
        {
            'Driver_ID': 'DRV-001',
            'Driver': 'Dragan Marković',
            'City': 'Belgrade',
            'Years_Exp': 12,
            'Safety_Score': 95,
            'Deliveries': 342,
            'Accidents': 0,
            'License': 'C',
            'Driver_Status': 'Active',
            'Contact': '+381 60 1234567'
        },
        {
            'Driver_ID': 'DRV-002',
            'Driver': 'Amar Hadžić',
            'City': 'Sarajevo',
            'Years_Exp': 8,
            'Safety_Score': 88,
            'Deliveries': 256,
            'Accidents': 1,
            'License': 'C',
            'Driver_Status': 'Active',
            'Contact': '+387 61 1234567'
        },
        {
            'Driver_ID': 'DRV-003',
            'Driver': 'Luka Vuković',
            'City': 'Zagreb',
            'Years_Exp': 15,
            'Safety_Score': 92,
            'Deliveries': 478,
            'Accidents': 0,
            'License': 'C',
            'Driver_Status': 'Active',
            'Contact': '+385 91 1234567'
        },
        {
            'Driver_ID': 'DRV-004',
            'Driver': 'Edin Džamić',
            'City': 'Skopje',
            'Years_Exp': 6,
            'Safety_Score': 82,
            'Deliveries': 145,
            'Accidents': 2,
            'License': 'C',
            'Driver_Status': 'On Leave',
            'Contact': '+389 70 1234567'
        },
        {
            'Driver_ID': 'DRV-005',
            'Driver': 'Bekim Shala',
            'City': 'Pristina',
            'Years_Exp': 10,
            'Safety_Score': 90,
            'Deliveries': 298,
            'Accidents': 0,
            'License': 'C',
            'Driver_Status': 'Active',
            'Contact': '+383 44 1234567'
        }
    ])

if 'fleet_data' not in st.session_state:
    st.session_state.fleet_data = pd.DataFrame([
        {
            'Truck_ID': 'PR-102-AL',
            'Driver_ID': 'DRV-001',
            'Model': 'Volvo FH16',
            'City': 'Pristina',
            'lat': 42.66,
            'lon': 21.16,
            'Status': 'Active',
            'Fuel': 85,
            'Route': 'Pristina → Belgrade',
            'ETD': '14:00',
            'Actual': '13:55',
            'Mileage': 125430,
            'Speed': 85,
            'Engine_Health': 95,
            'Tire_Condition': 92,
            'Next_Service': '2025-06-15',
            'Insurance_Exp': '2026-12-31',
            'Max_Capacity': 25000
        },
        {
            'Truck_ID': 'BG-550-TX',
            'Driver_ID': 'DRV-002',
            'Model': 'Mercedes Actros',
            'City': 'Belgrade',
            'lat': 44.78,
            'lon': 20.44,
            'Status': 'Active',
            'Fuel': 42,
            'Route': 'Belgrade → Skopje',
            'ETD': '18:30',
            'Actual': '18:45',
            'Mileage': 89650,
            'Speed': 78,
            'Engine_Health': 88,
            'Tire_Condition': 85,
            'Next_Service': '2025-05-20',
            'Insurance_Exp': '2025-11-30',
            'Max_Capacity': 24000
        },
        {
            'Truck_ID': 'ZG-991-HR',
            'Driver_ID': 'DRV-003',
            'Model': 'Scania R580',
            'City': 'Zagreb',
            'lat': 45.81,
            'lon': 15.98,
            'Status': 'Maintenance',
            'Fuel': 91,
            'Route': 'Zagreb → Split',
            'ETD': '12:00',
            'Actual': '12:05',
            'Mileage': 201230,
            'Speed': 0,
            'Engine_Health': 76,
            'Tire_Condition': 68,
            'Next_Service': '2025-04-10',
            'Insurance_Exp': '2026-03-15',
            'Max_Capacity': 26000
        },
        {
            'Truck_ID': 'SJ-442-BA',
            'Driver_ID': 'DRV-004',
            'Model': 'MAN TGX',
            'City': 'Sarajevo',
            'lat': 43.85,
            'lon': 18.41,
            'Status': 'Low Fuel',
            'Fuel': 12,
            'Route': 'Sarajevo → Tirana',
            'ETD': '09:00',
            'Actual': '09:30',
            'Mileage': 154890,
            'Speed': 92,
            'Engine_Health': 91,
            'Tire_Condition': 88,
            'Next_Service': '2025-07-01',
            'Insurance_Exp': '2026-08-20',
            'Max_Capacity': 23500
        },
        {
            'Truck_ID': 'SK-110-MK',
            'Driver_ID': 'DRV-005',
            'Model': 'Iveco Stralis',
            'City': 'Skopje',
            'lat': 41.99,
            'lon': 21.42,
            'Status': 'Active',
            'Fuel': 77,
            'Route': 'Skopje → Pristina',
            'ETD': '11:00',
            'Actual': '10:50',
            'Mileage': 98760,
            'Speed': 72,
            'Engine_Health': 89,
            'Tire_Condition': 91,
            'Next_Service': '2025-05-28',
            'Insurance_Exp': '2026-02-14',
            'Max_Capacity': 22000
        }
    ])

if 'shipments_data' not in st.session_state:
    st.session_state.shipments_data = pd.DataFrame([
        {
            'Shipment_ID': 'SHP-001',
            'Truck_ID': 'PR-102-AL',
            'Origin': 'Pristina',
            'Destination': 'Belgrade',
            'Cargo_Type': 'Electronics',
            'Weight': 2500,
            'Status': 'In Transit',
            'Progress': 65,
            'Priority': 'High',
            'Created': '2025-01-10 08:30',
            'Estimated_Delivery': '2025-01-11 14:00'
        },
        {
            'Shipment_ID': 'SHP-002',
            'Truck_ID': 'BG-550-TX',
            'Origin': 'Belgrade',
            'Destination': 'Skopje',
            'Cargo_Type': 'Food Products',
            'Weight': 5000,
            'Status': 'Pending',
            'Progress': 0,
            'Priority': 'Medium',
            'Created': '2025-01-10 09:15',
            'Estimated_Delivery': '2025-01-12 10:00'
        },
        {
            'Shipment_ID': 'SHP-003',
            'Truck_ID': 'ZG-991-HR',
            'Origin': 'Zagreb',
            'Destination': 'Split',
            'Cargo_Type': 'Machinery',
            'Weight': 8500,
            'Status': 'Delayed',
            'Progress': 40,
            'Priority': 'High',
            'Created': '2025-01-09 14:20',
            'Estimated_Delivery': '2025-01-11 16:00'
        },
        {
            'Shipment_ID': 'SHP-004',
            'Truck_ID': 'SJ-442-BA',
            'Origin': 'Sarajevo',
            'Destination': 'Tirana',
            'Cargo_Type': 'Textiles',
            'Weight': 3200,
            'Status': 'In Transit',
            'Progress': 35,
            'Priority': 'Low',
            'Created': '2025-01-10 06:00',
            'Estimated_Delivery': '2025-01-12 18:00'
        },
        {
            'Shipment_ID': 'SHP-005',
            'Truck_ID': 'SK-110-MK',
            'Origin': 'Skopje',
            'Destination': 'Pristina',
            'Cargo_Type': 'Raw Materials',
            'Weight': 6800,
            'Status': 'Delivered',
            'Progress': 100,
            'Priority': 'Medium',
            'Created': '2025-01-09 10:30',
            'Estimated_Delivery': '2025-01-10 16:30'
        },
        {
            'Shipment_ID': 'SHP-006',
            'Truck_ID': 'PR-102-AL',
            'Origin': 'Belgrade',
            'Destination': 'Niš',
            'Cargo_Type': 'Automotive Parts',
            'Weight': 4100,
            'Status': 'Pending',
            'Progress': 0,
            'Priority': 'High',
            'Created': '2025-01-10 07:45',
            'Estimated_Delivery': '2025-01-11 18:00'
        }
    ])

if 'maintenance_data' not in st.session_state:
    st.session_state.maintenance_data = pd.DataFrame([
        {
            'Truck_ID': 'PR-102-AL',
            'Service_Type': 'Oil Change',
            'Date': '2025-01-05',
            'Cost': 250,
            'Status': 'Completed',
            'Mileage': 125200,
            'Notes': 'Routine maintenance'
        },
        {
            'Truck_ID': 'BG-550-TX',
            'Service_Type': 'Tire Replacement',
            'Date': '2025-01-03',
            'Cost': 1200,
            'Status': 'Completed',
            'Mileage': 89100,
            'Notes': 'All 4 tires replaced'
        },
        {
            'Truck_ID': 'ZG-991-HR',
            'Service_Type': 'Engine Diagnostic',
            'Date': '2025-01-10',
            'Cost': 450,
            'Status': 'In Progress',
            'Mileage': 201200,
            'Notes': 'Engine health monitoring'
        },
        {
            'Truck_ID': 'SJ-442-BA',
            'Service_Type': 'Brake Inspection',
            'Date': '2024-12-28',
            'Cost': 350,
            'Status': 'Completed',
            'Mileage': 154500,
            'Notes': 'Front and rear brakes checked'
        },
        {
            'Truck_ID': 'SK-110-MK',
            'Service_Type': 'Filter Replacement',
            'Date': '2025-01-08',
            'Cost': 180,
            'Status': 'Completed',
            'Mileage': 98500,
            'Notes': 'Air and fuel filters replaced'
        }
    ])

def simulate_live_data():
    # Update fleet data positions and statuses
    for idx in st.session_state.fleet_data.index:
        if st.session_state.fleet_data.loc[idx, 'Status'] in ['Active', 'Low Fuel']:
            st.session_state.fleet_data.loc[idx, 'lat'] += random.uniform(-0.02, 0.02)
            st.session_state.fleet_data.loc[idx, 'lon'] += random.uniform(-0.02, 0.02)
            st.session_state.fleet_data.loc[idx, 'Fuel'] = max(5, st.session_state.fleet_data.loc[idx, 'Fuel'] - random.uniform(0.5, 2))
            st.session_state.fleet_data.loc[idx, 'Speed'] = random.randint(40, 120)
            st.session_state.fleet_data.loc[idx, 'Mileage'] += random.uniform(0.5, 3)
            
            if st.session_state.fleet_data.loc[idx, 'Fuel'] < 15 and st.session_state.fleet_data.loc[idx, 'Status'] != 'Low Fuel':
                st.session_state.fleet_data.loc[idx, 'Status'] = 'Low Fuel'
            elif st.session_state.fleet_data.loc[idx, 'Fuel'] > 30 and st.session_state.fleet_data.loc[idx, 'Status'] == 'Low Fuel':
                st.session_state.fleet_data.loc[idx, 'Status'] = 'Active'
    # Update shipment progress
    for idx in st.session_state.shipments_data.index:
        if st.session_state.shipments_data.loc[idx, 'Status'] == 'In Transit':
            st.session_state.shipments_data.loc[idx, 'Progress'] = min(100, st.session_state.shipments_data.loc[idx, 'Progress'] + random.uniform(0.5, 3))
            if st.session_state.shipments_data.loc[idx, 'Progress'] >= 100:
                st.session_state.shipments_data.loc[idx, 'Status'] = 'Delivered'
            elif random.random() < 0.02:
                st.session_state.shipments_data.loc[idx, 'Status'] = 'Delayed'

# Run simulation on each refresh
simulate_live_data()



with st.sidebar:
    st.markdown("<h2 style='color: #ffffff; margin-bottom: 10px;'>🚚 OMNILogistics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8a92a4; margin-bottom: 20px; font-size: 0.9rem;'>Balkan Fleet Hub</p>", unsafe_allow_html=True)
    
    st.divider()
    
    page = st.radio(
        "📍 NAVIGATION",
        [
            "Dashboard",
            "Trucks",
            "Drivers",
            "Shipments",
            "Maintenance",
            "Analytics"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    active_trucks = len(st.session_state.fleet_data[st.session_state.fleet_data['Status'] == 'Active'])
    in_transit = len(st.session_state.shipments_data[st.session_state.shipments_data['Status'] == 'In Transit'])
    
    st.markdown(f"""
    <div class="metric-card">
    <h4 style='margin: 0 0 12px 0; color: #ffffff;'>⚡ Live Status</h4>
    <p style='margin: 6px 0; color: #22c55e; font-weight: 600;'>✓ Active: {active_trucks}/{len(st.session_state.fleet_data)}</p>
    <p style='margin: 6px 0; color: #60a5fa; font-weight: 600;'>📦 In Transit: {in_transit}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🟢 OMNI v2.0 | Real-time Active", icon="ℹ️")

merged_data = st.session_state.fleet_data.merge(
    st.session_state.drivers_data,
    on="Driver_ID",
    how="left"
)

if page == "Dashboard":
    st.markdown("<h1 style='margin-bottom: 30px;'>📊 Operations Control Center</h1>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("🚚 Active Trucks", len(st.session_state.fleet_data[st.session_state.fleet_data['Status'] == 'Active']))
    with c2:
        st.metric("📦 In Transit", len(st.session_state.shipments_data[st.session_state.shipments_data['Status'] == 'In Transit']))
    with c3:
        st.metric("✅ Delivered", len(st.session_state.shipments_data[st.session_state.shipments_data['Status'] == 'Delivered']))
    with c4:
        st.metric("⚠️ Critical", len(st.session_state.fleet_data[st.session_state.fleet_data['Fuel'] < 20]))
    
    st.markdown("<h2 style='margin-top: 30px; margin-bottom: 20px;'>🗺️ Live GPS Fleet Tracking</h2>", unsafe_allow_html=True)
    
    fig = go.Figure()
    
    for _, row in merged_data.iterrows():
        color_map = {'Active': 'green', 'Maintenance': 'orange', 'Low Fuel': 'red', 'Inactive': 'gray'}
        marker_color = color_map.get(row['Status'], 'blue')
        driver_name = str(row['Driver']) if pd.notna(row['Driver']) else "Unassigned"
        
        fig.add_trace(
            go.Scattermapbox(
                lat=[row["lat"]],
                lon=[row["lon"]],
                mode="markers+text",
                text=[row["Truck_ID"]],
                textposition="top center",
                marker=go.scattermapbox.Marker(size=16, color=marker_color, opacity=0.9),
                hovertemplate=f"""
                <b style='color: #fff;'>Truck:</b> {row['Truck_ID']}<br>
                <b style='color: #fff;'>Driver:</b> {driver_name}<br>
                <b style='color: #fff;'>Route:</b> {row['Route']}<br>
                <b style='color: #fff;'>Fuel:</b> {row['Fuel']:.0f}%<br>
                <b style='color: #fff;'>Speed:</b> {row['Speed']} km/h<br>
                <b style='color: #fff;'>Status:</b> {row['Status']}<br>
                <extra></extra>
                """
            )
        )
    
    fig.update_layout(
        mapbox=dict(style="carto-darkmatter", center=dict(lat=44.0, lon=20.5), zoom=5),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template="plotly_dark",
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<h3 style='margin-bottom: 15px;'>📋 Recent Shipments</h3>", unsafe_allow_html=True)
        recent_ships = st.session_state.shipments_data.sort_values('Created', ascending=False).head(5)[['Shipment_ID', 'Origin', 'Destination', 'Status', 'Progress']]
        st.dataframe(recent_ships, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("<h3 style='margin-bottom: 15px;'>🚨 Upcoming Maintenance</h3>", unsafe_allow_html=True)
        maint = st.session_state.fleet_data[['Truck_ID', 'Next_Service', 'Engine_Health']].sort_values('Engine_Health').head(5)
        st.dataframe(maint, use_container_width=True, hide_index=True)
    
    with col3:
        st.markdown("<h3 style='margin-bottom: 15px;'>📊 Fleet Status</h3>", unsafe_allow_html=True)
        status_counts = st.session_state.fleet_data['Status'].value_counts()
        fig_pie = px.pie(values=status_counts.values, names=status_counts.index, color_discrete_sequence=['#ffffff', '#a1a1aa', '#52525b', '#27272a'])
        fig_pie.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

elif page == "Trucks":
    st.markdown("<h1 style='margin-bottom: 30px;'>🚚 Fleet Management</h1>", unsafe_allow_html=True)
    
    # Add new truck section
    st.markdown("<h2 style='margin-bottom: 20px; color: #ffffff;'>➕ Add New Truck</h2>", unsafe_allow_html=True)
    
    col_form1, col_form2 = st.columns(2)
    
    with col_form1:
        with st.form("add_truck_form"):
            new_truck_id = st.text_input("Truck ID (e.g., PR-103-AL)", placeholder="PR-103-AL")
            new_truck_model = st.text_input("Model", placeholder="Volvo FH16")
            new_truck_city = st.selectbox("Current City", list(BALKAN_CITIES.keys()), key="new_truck_city")
            new_truck_driver = st.selectbox("Assign Driver", st.session_state.drivers_data['Driver_ID'].values, key="new_truck_driver")
            new_truck_capacity = st.number_input("Max Capacity (kg)", 15000, 30000, 22000)
            new_truck_fuel = st.slider("Initial Fuel Level", 0, 100, 80)
            new_truck_route = st.text_input("Route", placeholder="City1 → City2")
            new_truck_status = st.selectbox("Status", ["Active", "Maintenance", "Inactive"], key="new_truck_status")
            
            submit_truck = st.form_submit_button("✅ Add Truck", use_container_width=True)
            
            if submit_truck:
                if new_truck_id and new_truck_model:
                    # Check for duplicate Truck ID
                    if new_truck_id in st.session_state.fleet_data['Truck_ID'].values:
                        st.error(f"❌ Truck ID {new_truck_id} already exists!")
                    else:
                        city_coords = BALKAN_CITIES[new_truck_city]
                        new_truck = pd.DataFrame([{
                            'Truck_ID': new_truck_id,
                            'Driver_ID': new_truck_driver,
                            'Model': new_truck_model,
                            'City': new_truck_city,
                            'lat': city_coords[0],
                            'lon': city_coords[1],
                            'Status': new_truck_status,
                            'Fuel': new_truck_fuel,
                            'Route': new_truck_route,
                            'ETD': '00:00',
                            'Actual': '00:00',
                            'Mileage': 0,
                            'Speed': 0,
                            'Engine_Health': 95,
                            'Tire_Condition': 95,
                            'Next_Service': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
                            'Insurance_Exp': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
                            'Max_Capacity': new_truck_capacity
                        }])
                        st.session_state.fleet_data = pd.concat([st.session_state.fleet_data, new_truck], ignore_index=True)
                        st.success(f"✅ Truck {new_truck_id} added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill in Truck ID and Model")
    
    with col_form2:
        st.info("📝 Fill in the form to add a new truck to the fleet", icon="ℹ️")
    
    st.divider()
    
    # Delete truck section
    st.markdown("<h2 style='margin-bottom: 20px; color: #ef4444;'>🗑️ Remove Truck</h2>", unsafe_allow_html=True)
    
    col_del1, col_del2 = st.columns(2)
    
    with col_del1:
        truck_to_delete = st.selectbox("Select Truck to Delete", st.session_state.fleet_data['Truck_ID'].unique(), key="delete_truck")
        if st.button("🗑️ Delete Truck", use_container_width=True, key="btn_delete_truck"):
            truck_model = st.session_state.fleet_data[st.session_state.fleet_data['Truck_ID'] == truck_to_delete]['Model'].values[0]
            st.session_state.fleet_data = st.session_state.fleet_data[st.session_state.fleet_data['Truck_ID'] != truck_to_delete]
            st.success(f"✅ Truck {truck_to_delete} ({truck_model}) deleted!")
            st.rerun()
    
    with col_del2:
        st.error("⚠️ This action cannot be undone", icon="❌")
    
    st.divider()
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("<h3 style='margin-bottom: 15px;'>Fleet Registry</h3>", unsafe_allow_html=True)
        selected_truck = st.selectbox("Select Truck", st.session_state.fleet_data['Truck_ID'].unique(), label_visibility="collapsed")
        truck_data = merged_data[merged_data['Truck_ID'] == selected_truck].iloc[0]
    
    with col2:
        st.markdown(f"<h3 style='margin-bottom: 15px;'>📋 Details - {selected_truck}</h3>", unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Model", truck_data['Model'])
            st.metric("Mileage", f"{truck_data['Mileage']:,.0f} km")
        with c2:
            st.metric("Fuel", f"{truck_data['Fuel']:.0f}%")
            st.metric("Speed", f"{truck_data['Speed']} km/h")
        with c3:
            st.metric("Engine", f"{truck_data['Engine_Health']}%")
            st.metric("Tires", f"{truck_data['Tire_Condition']}%")
        with c4:
            driver_name = str(truck_data.get('Driver', 'Unassigned')) if pd.notna(truck_data.get('Driver')) else "Unassigned"
            st.metric("Driver", driver_name[:20])
            st.metric("Status", truck_data['Status'])
        
        st.divider()
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Capacity", f"{truck_data['Max_Capacity']:,.0f} kg")
        with c2:
            st.metric("Insurance", truck_data['Insurance_Exp'])
        with c3:
            st.metric("Next Service", truck_data['Next_Service'])
        
        st.divider()
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<h4 style='margin-bottom: 15px;'>📦 Active Shipments</h4>", unsafe_allow_html=True)
            shipments = st.session_state.shipments_data[st.session_state.shipments_data['Truck_ID'] == selected_truck]
            if not shipments.empty:
                for _, ship in shipments.iterrows():
                    status_color = 'green' if ship['Status'] == 'Delivered' else 'orange' if ship['Status'] == 'Delayed' else 'blue'
                    st.markdown(f"""
                    <div class="metric-card">
                    <p style='margin: 0 0 5px 0; color: #ffffff; font-weight: 600;'>📦 {ship['Shipment_ID']}</p>
                    <p style='margin: 0 0 8px 0; color: #b4bcc8;'>{ship['Origin']} → {ship['Destination']}</p>
                    <span class="badge badge-{status_color}">{ship['Status']}</span>
                    <p style='margin: 8px 0 0 0; color: #8a92a4; font-size: 0.85rem;'>Progress: {ship['Progress']:.0f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No active shipments")
        
        with col2:
            st.markdown("<h4 style='margin-bottom: 15px;'>🔧 Service History</h4>", unsafe_allow_html=True)
            services = st.session_state.maintenance_data[st.session_state.maintenance_data['Truck_ID'] == selected_truck]
            if not services.empty:
                st.dataframe(services[['Service_Type', 'Date', 'Cost', 'Status']].tail(5), use_container_width=True, hide_index=True)
            else:
                st.info("No service records")

elif page == "Drivers":
    st.markdown("<h1 style='margin-bottom: 30px;'>👥 Driver Management</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        col1a, col1b, col1c = st.columns(3)
        
        with col1a:
            st.metric("👥 Total Drivers", len(st.session_state.drivers_data))
        with col1b:
            active = len(st.session_state.drivers_data[st.session_state.drivers_data['Driver_Status'] == 'Active'])
            st.metric("✓ Active", active)
        with col1c:
            avg_score = st.session_state.drivers_data['Safety_Score'].mean()
            st.metric("Avg Safety Score", f"{avg_score:.0f}%")
    
    with col2:
        st.markdown("<h3 style='color: #ffffff;'>➕ Add New Driver</h3>", unsafe_allow_html=True)
        with st.form("add_driver_form"):
            new_driver_id = st.text_input("Driver ID (e.g., DRV-006)", placeholder="DRV-006")
            new_driver_name = st.text_input("Full Name", placeholder="John Doe")
            new_driver_city = st.selectbox("Home City", list(BALKAN_CITIES.keys()))
            new_driver_exp = st.slider("Years of Experience", 0, 40, 5)
            new_driver_license = st.selectbox("License Category", ["A", "B", "C", "D"])
            new_driver_contact = st.text_input("Contact Number", placeholder="+381 60 1234567")
            new_driver_status = st.selectbox("Status", ["Active", "On Leave", "Inactive"])
            
            submit_driver = st.form_submit_button("✅ Add Driver", use_container_width=True)
            
            if submit_driver:
                if new_driver_id and new_driver_name:
                    # Check for duplicate Driver ID
                    if new_driver_id in st.session_state.drivers_data['Driver_ID'].values:
                        st.error(f"❌ Driver ID {new_driver_id} already exists!")
                    else:
                        new_driver = pd.DataFrame([{
                            'Driver_ID': new_driver_id,
                            'Driver': new_driver_name,
                            'City': new_driver_city,
                            'Years_Exp': new_driver_exp,
                            'Safety_Score': random.randint(75, 99),
                            'Deliveries': 0,
                            'Accidents': 0,
                            'License': new_driver_license,
                            'Driver_Status': new_driver_status,
                            'Contact': new_driver_contact
                        }])
                        st.session_state.drivers_data = pd.concat([st.session_state.drivers_data, new_driver], ignore_index=True)
                        st.success(f"✅ Driver {new_driver_name} added successfully!")
                        st.rerun()
                else:
                    st.error("Please fill in Driver ID and Name")
    
    st.divider()
    st.markdown("<h2 style='margin-bottom: 20px;'>👤 Driver Profiles</h2>", unsafe_allow_html=True)
    
    # Delete driver section
    col_delete = st.columns(1)[0]
    with col_delete:
        st.markdown("<h3 style='color: #ef4444;'>🗑️ Remove Driver</h3>", unsafe_allow_html=True)
        driver_to_delete = st.selectbox("Select Driver to Delete", st.session_state.drivers_data['Driver_ID'].unique(), key="delete_driver")
        
        col_del1, col_del2 = st.columns(2)
        with col_del1:
            if st.button("🗑️ Delete Driver", use_container_width=True, key="btn_delete_driver"):
                driver_name = st.session_state.drivers_data[st.session_state.drivers_data['Driver_ID'] == driver_to_delete]['Driver'].values[0]
                st.session_state.drivers_data = st.session_state.drivers_data[st.session_state.drivers_data['Driver_ID'] != driver_to_delete]
                st.success(f"✅ Driver {driver_name} ({driver_to_delete}) deleted!")
                st.rerun()
        with col_del2:
            st.info("⚠️ This action cannot be undone", icon="⚠️")
    
    st.divider()
    
    for _, driver in st.session_state.drivers_data.iterrows():
        col1, col2 = st.columns([0.5, 2])
        
        with col1:
            st.markdown(f"<div style='font-size: 2.5rem; text-align: center;'>👤</div>", unsafe_allow_html=True)
        
        with col2:
            safety_color = 'green' if driver['Safety_Score'] >= 90 else 'orange' if driver['Safety_Score'] >= 80 else 'red'
            status_color = 'green' if driver['Driver_Status'] == 'Active' else 'orange'
            st.markdown(f"""
            <div class="metric-card">
            <h4 style='margin: 0 0 5px 0; color: #e8eef5;'>{driver['Driver']}</h4>
            <p style='margin: 0 0 12px 0; color: #8a92a4; font-size: 0.85rem;'>{driver['Driver_ID']} | {driver['City']}</p>
            <p style='margin: 8px 0; color: #b4bcc8;'>📚 Experience: <span style='color: #e8eef5; font-weight: 600;'>{driver['Years_Exp']} years</span> | 📜 License: <span style='color: #e8eef5; font-weight: 600;'>{driver['License']}</span></p>
            <p style='margin: 8px 0; color: #b4bcc8;'>✅ Deliveries: <span style='color: #22c55e; font-weight: 600;'>{driver['Deliveries']}</span> | ⚠️ Accidents: <span style='color: #ef4444; font-weight: 600;'>{driver['Accidents']}</span></p>
            <p style='margin: 8px 0; color: #b4bcc8;'>📞 {driver['Contact']}</p>
            <div style='margin-top: 10px;'>
                <span class="badge badge-{safety_color}">Safety: {driver['Safety_Score']}%</span>
                <span class="badge badge-{status_color}">{driver['Driver_Status']}</span>
            </div>
            </div>
            """, unsafe_allow_html=True)

elif page == "Shipments":
    st.markdown("<h1 style='margin-bottom: 30px;'>📦 Shipment Tracking</h1>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📦 Total", len(st.session_state.shipments_data))
    with c2:
        st.metric("🚚 In Transit", len(st.session_state.shipments_data[st.session_state.shipments_data['Status'] == 'In Transit']))
    with c3:
        st.metric("✅ Delivered", len(st.session_state.shipments_data[st.session_state.shipments_data['Status'] == 'Delivered']))
    with c4:
        st.metric("🔴 Delayed", len(st.session_state.shipments_data[st.session_state.shipments_data['Status'] == 'Delayed']))
    
    st.markdown("<h2 style='margin-top: 30px; margin-bottom: 20px;'>📋 Active Shipments</h2>", unsafe_allow_html=True)
    
    for _, shipment in st.session_state.shipments_data.iterrows():
        status_color = {'In Transit': 'blue', 'Delivered': 'green', 'Delayed': 'red', 'Pending': 'orange'}
        color = status_color.get(shipment['Status'], 'orange')
        priority_color = 'red' if shipment['Priority'] == 'High' else 'orange' if shipment['Priority'] == 'Medium' else 'green'
        
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom: 16px;">
        <h4 style='margin: 0 0 8px 0; color: #ffffff;'>{shipment['Shipment_ID']}</h4>
        <p style='margin: 8px 0; color: #b4bcc8;'>📍 {shipment['Origin']} → {shipment['Destination']} | 📦 {shipment['Cargo_Type']}</p>
        <p style='margin: 8px 0; color: #b4bcc8;'>⚖️ Weight: <span style='color: #e8eef5; font-weight: 600;'>{shipment['Weight']:,} kg</span> | 🚚 Truck: <span style='color: #e8eef5; font-weight: 600;'>{shipment['Truck_ID']}</span></p>
        <div style="margin: 12px 0;">
            <span class="badge badge-{color}">Status: {shipment['Status']}</span>
            <span class="badge badge-{priority_color}">Priority: {shipment['Priority']}</span>
        </div>
        <p style='margin: 8px 0; color: #8a92a4; font-size: 0.85rem;'>ETA: {shipment['Estimated_Delivery']}</p>
        
        <!-- Custom Progress Bar -->
        <div style="background-color: var(--border); border-radius: 4px; height: 6px; width: 100%; margin-top: 12px; overflow: hidden;">
            <div style="background-color: var(--accent); height: 100%; width: {shipment['Progress']:.0f}%; transition: width 0.5s ease-in-out;"></div>
        </div>
        <p style="margin: 4px 0 0 0; color: var(--text-tertiary); font-size: 0.75rem; text-align: right;">Progress: {shipment['Progress']:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "Maintenance":
    st.markdown("<h1 style='margin-bottom: 30px;'>🔧 Maintenance & Audits</h1>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='margin-bottom: 20px;'>📅 Service Schedule</h2>", unsafe_allow_html=True)
    
    for _, truck in st.session_state.fleet_data.iterrows():
        service_date = datetime.strptime(truck['Next_Service'], '%Y-%m-%d')
        days_until = (service_date - datetime.now()).days
        
        status_badge = 'red' if days_until < 0 else 'orange' if days_until < 7 else 'green'
        status_text = 'OVERDUE' if days_until < 0 else 'URGENT' if days_until < 7 else 'SCHEDULED'
        
        st.markdown(f"""
        <div class="metric-card">
        <h4 style='margin: 0 0 8px 0; color: #e8eef5;'>{truck['Truck_ID']} - {truck['Model']}</h4>
        <p style='margin: 6px 0; color: #b4bcc8;'>🏥 Engine Health: <span style='color: #e8eef5; font-weight: 600;'>{truck['Engine_Health']}%</span> | 🔘 Tire Condition: <span style='color: #e8eef5; font-weight: 600;'>{truck['Tire_Condition']}%</span></p>
        <p style='margin: 6px 0; color: #b4bcc8;'>📅 Next Service: <span style='color: #e8eef5; font-weight: 600;'>{truck['Next_Service']} ({days_until} days)</span></p>
        <span class="badge badge-{status_badge}">{status_text}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='margin-top: 30px; margin-bottom: 20px;'>📋 Recent Services</h2>", unsafe_allow_html=True)
    maint_df = st.session_state.maintenance_data.copy()
    st.dataframe(maint_df[['Truck_ID', 'Service_Type', 'Date', 'Cost', 'Status', 'Notes']], use_container_width=True, hide_index=True)
    
    st.markdown("<h3 style='margin-top: 20px;'>Total Maintenance Costs</h3>", unsafe_allow_html=True)
    st.metric("💰", f"${st.session_state.maintenance_data['Cost'].sum():,.0f}")

elif page == "Analytics":
    st.markdown("<h1 style='margin-bottom: 30px;'>📈 Fleet Intelligence</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        avg_fuel = st.session_state.fleet_data['Fuel'].mean()
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_fuel,
            title={'text': "Avg Fuel %"},
            gauge={
                'bar': {'color': "#ffffff"}, 
                'axis': {'range': [0, 100]},
                'threshold': {
                    'line': {'color': 'red'}, 
                    'thickness': 0.2, 
                    'value': 20
                }
            }
        ))
        fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        status_counts = st.session_state.fleet_data['Status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, title="Fleet Status", color_discrete_sequence=['#ffffff', '#a1a1aa', '#52525b', '#27272a'])
        fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    with c3:
        city_counts = st.session_state.fleet_data['City'].value_counts()
        fig = px.bar(x=city_counts.index, y=city_counts.values, title="Trucks per City", color_discrete_sequence=['#ffffff'])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor='rgba(0,0,0,0)', template="plotly_dark", showlegend=False, height=300)
        fig.update_xaxes(title_text="City")
        fig.update_yaxes(title_text="Number of Trucks")
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⚙️ Avg Engine Health", f"{st.session_state.fleet_data['Engine_Health'].mean():.0f}%")
    with col2:
        st.metric("🔘 Avg Tire Condition", f"{st.session_state.fleet_data['Tire_Condition'].mean():.0f}%")
    with col3:
        total_cost = st.session_state.maintenance_data['Cost'].sum()
        st.metric("💰 Total Maintenance", f"${total_cost:,.0f}")
    
    st.markdown("<h2 style='margin-top: 30px; margin-bottom: 20px;'>📊 Shipment Statistics</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        status_ship = st.session_state.shipments_data['Status'].value_counts()
        fig = px.bar(x=status_ship.index, y=status_ship.values, title="Shipments by Status", color_discrete_sequence=['#ffffff', '#a1a1aa', '#52525b', '#27272a'])
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor='rgba(0,0,0,0)', template="plotly_dark", showlegend=False)
        fig.update_xaxes(title_text="Status")
        fig.update_yaxes(title_text="Number of Shipments")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        priority_ship = st.session_state.shipments_data['Priority'].value_counts()
        fig = px.pie(values=priority_ship.values, names=priority_ship.index, title="Shipments by Priority", color_discrete_sequence=['#52525b', '#a1a1aa', '#ffffff'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("<p style='text-align: center; color: #8a92a4; font-size: 0.85rem; margin: 20px 0;'>🚚 OMNI Logistics Dashboard © 2026 | Real-time Fleet Management System | Balkan Operations Hub</p>", unsafe_allow_html=True)

