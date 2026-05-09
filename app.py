import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings

# --- 1. SETUP & THEME ---
st.set_page_config(
    page_title="OMNI Balkan Hub",
    layout="wide",
    page_icon="🚛"
)

warnings.filterwarnings("ignore")

# --- 2. DATA INITIALIZATION ---

# DRIVERS DATABASE
if 'drivers_data' not in st.session_state:
    st.session_state.drivers_data = pd.DataFrame([
        {'Driver_ID': 'DRV-001', 'Driver': 'Dragan P.'},
        {'Driver_ID': 'DRV-002', 'Driver': 'Amar H.'},
        {'Driver_ID': 'DRV-003', 'Driver': 'Luka V.'},
        {'Driver_ID': 'DRV-004', 'Driver': 'Edin D.'},
        {'Driver_ID': 'DRV-005', 'Driver': 'Bekim S.'}
    ])

# TRUCKS DATABASE
if 'fleet_data' not in st.session_state:
    st.session_state.fleet_data = pd.DataFrame([
        {
            'Truck_ID': 'PR-102-AL',
            'Driver_ID': 'DRV-001',
            'City': 'Pristina',
            'lat': 42.66,
            'lon': 21.16,
            'Status': 'Active',
            'Fuel': 85,
            'Route': 'Prishtina -> Belgrade',
            'ETD': '14:00',
            'Actual': '13:55'
        },
        {
            'Truck_ID': 'BG-550-TX',
            'Driver_ID': 'DRV-002',
            'City': 'Belgrade',
            'lat': 44.78,
            'lon': 20.44,
            'Status': 'Active',
            'Fuel': 42,
            'Route': 'Belgrade -> Skopje',
            'ETD': '18:30',
            'Actual': '18:45'
        },
        {
            'Truck_ID': 'ZG-991-HR',
            'Driver_ID': 'DRV-003',
            'City': 'Zagreb',
            'lat': 45.81,
            'lon': 15.98,
            'Status': 'Maintenance',
            'Fuel': 91,
            'Route': 'Zagreb -> Sarajevo',
            'ETD': '12:00',
            'Actual': '12:05'
        },
        {
            'Truck_ID': 'SJ-442-BA',
            'Driver_ID': 'DRV-004',
            'City': 'Sarajevo',
            'lat': 43.85,
            'lon': 18.41,
            'Status': 'Active',
            'Fuel': 12,
            'Route': 'Sarajevo -> Tirana',
            'ETD': '09:00',
            'Actual': '09:30'
        },
        {
            'Truck_ID': 'SK-110-MK',
            'Driver_ID': 'DRV-005',
            'City': 'Skopje',
            'lat': 41.99,
            'lon': 21.42,
            'Status': 'Active',
            'Fuel': 77,
            'Route': 'Skopje -> Prishtina',
            'ETD': '11:00',
            'Actual': '10:50'
        }
    ])

# --- 3. CUSTOM CSS ---
st.markdown("""
<style>

.stApp {
    background-color: #f8fafc !important;
}

h1, h2, h3, h4, p, label, [data-testid="stMetricValue"] {
    color: #0f172a !important;
}

[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0;
}

[data-testid="stSidebar"] * {
    color: #1e293b !important;
}

.stButton>button {
    background-color: #f97316 !important;
    color: white !important;
    width: 100%;
    border: none;
    font-weight: bold;
    height: 3.5em;
}

.audit-box {
    background-color: #0f172a;
    color: #22c55e;
    padding: 20px;
    border-radius: 8px;
    font-family: monospace;
    border-left: 5px solid #f97316;
    margin-bottom: 12px;
    line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:

    st.markdown(
        "<h1 style='color: #f97316;'>OMNI</h1>",
        unsafe_allow_html=True
    )

    page = st.radio(
        "SYSTEM MENU",
        [
            "Dashboard",
            "Drivers",
            "Fleet Registry",
            "Audits",
            "Analytics"
        ]
    )

    st.divider()

    st.info("OMNI V1.0 | Regional Node Active")

# --- MERGED DATA ---
merged_data = st.session_state.fleet_data.merge(
    st.session_state.drivers_data,
    on="Driver_ID",
    how="left"
)
# --- 5. DASHBOARD ---
if page == "Dashboard":

    st.header("Operations Control")

    c1, c2, c3 = st.columns(3)

    c1.metric("Active Assets", len(st.session_state.fleet_data))
    c2.metric("Fleet Efficiency", "94%")
    c3.metric(
        "Critical Alerts",
        f"{len(st.session_state.fleet_data[st.session_state.fleet_data['Fuel'] < 20])} Low Fuel"
    )

    st.subheader("Live GPS Truck Tracking")

    # CREATE MAP
    fig = go.Figure()

    # ADD EACH TRUCK AS GPS POINT
    for _, row in merged_data.iterrows():

        fig.add_trace(
            go.Scattermapbox(
                lat=[row["lat"]],
                lon=[row["lon"]],
                mode="markers+text",

                # TRUCK LABEL ON MAP
                text=[row["Truck_ID"]],
                textposition="top center",

                # RED GPS CIRCLE
                marker=go.scattermapbox.Marker(
                    size=22,
                    color="red",
                    opacity=0.9
                ),

                # POPUP INFO
                hovertemplate=
                f"""
                <b>Truck:</b> {row['Truck_ID']}<br>
                <b>Driver:</b> {row['Driver']}<br>
                <b>Route:</b> {row['Route']}<br>
                <b>Fuel:</b> {row['Fuel']}%<br>
                <b>Status:</b> {row['Status']}<br>
                <b>City:</b> {row['City']}<br>
                <b>Latitude:</b> {row['lat']}<br>
                <b>Longitude:</b> {row['lon']}<br>
                <extra></extra>
                """
            )
        )

    # MAP SETTINGS
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",

            # CENTER MAP
            center=dict(
                lat=44.0,
                lon=20.5
            ),

            zoom=5
        ),

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        ),

        height=750,
        showlegend=False
    )

    # DISPLAY MAP
    st.plotly_chart(
        fig,
        use_container_width=True
    )
# --- 6. DRIVERS PORTAL ---
elif page == "Drivers":

    st.header("Drivers Portal")

    driver_ids = st.session_state.drivers_data['Driver_ID'].unique()

    selected_driver = st.selectbox(
        "Select Driver ID",
        driver_ids
    )

    driver_info = st.session_state.drivers_data[
        st.session_state.drivers_data['Driver_ID'] == selected_driver
    ]

    st.subheader("Driver Information")

    st.dataframe(
        driver_info,
        use_container_width=True
    )

    st.subheader("Assigned Trucks")

    driver_trucks = merged_data[
        merged_data['Driver_ID'] == selected_driver
    ]

    if not driver_trucks.empty:

        st.dataframe(
            driver_trucks[
                [
                    'Truck_ID',
                    'Driver',
                    'Route',
                    'Fuel',
                    'City',
                    'Status',
                    'ETD',
                    'Actual'
                ]
            ],
            use_container_width=True
        )

    else:
        st.warning("No trucks assigned to this driver.")

# --- 7. TRUCKS PORTAL ---
elif page == "Fleet Registry":

    st.header("Trucks Portal")

    st.subheader("Fleet Database")

    st.dataframe(
        merged_data[
            [
                'Truck_ID',
                'Driver',
                'Route',
                'Fuel',
                'City',
                'Status',
                'ETD',
                'Actual'
            ]
        ],
        use_container_width=True
    )

    st.divider()

    col1, col2 = st.columns(2)

    # ADD NEW TRUCK
    with col1:

        st.subheader("Add Truck")

        with st.form("add_truck_form"):

            new_truck_id = st.text_input("Truck ID")

            driver_options = st.session_state.drivers_data[
                ['Driver_ID', 'Driver']
            ]

            driver_selection = st.selectbox(
                "Assign Driver",
                driver_options.apply(
                    lambda x: f"{x['Driver_ID']} - {x['Driver']}",
                    axis=1
                )
            )

            selected_driver_id = driver_selection.split(" - ")[0]

            new_city = st.selectbox(
                "City",
                [
                    "Pristina",
                    "Belgrade",
                    "Skopje",
                    "Tirana",
                    "Sarajevo",
                    "Zagreb"
                ]
            )

            new_route = st.text_input("Route")
            new_fuel = st.slider("Fuel Level", 0, 100, 100)

            new_status = st.selectbox(
                "Status",
                [
                    "Active",
                    "Maintenance",
                    "Inactive"
                ]
            )

            new_etd = st.text_input("ETD", "00:00")
            new_actual = st.text_input("Actual", "00:00")

            submit_truck = st.form_submit_button("REGISTER TRUCK")

            if submit_truck:

                coords = {
                    "Pristina": (42.66, 21.16),
                    "Belgrade": (44.78, 20.44),
                    "Skopje": (41.99, 21.42),
                    "Tirana": (41.32, 19.81),
                    "Sarajevo": (43.85, 18.41),
                    "Zagreb": (45.81, 15.98)
                }

                lat, lon = coords[new_city]

                new_row = pd.DataFrame([
                    {
                        'Truck_ID': new_truck_id,
                        'Driver_ID': selected_driver_id,
                        'City': new_city,
                        'lat': lat,
                        'lon': lon,
                        'Status': new_status,
                        'Fuel': new_fuel,
                        'Route': new_route,
                        'ETD': new_etd,
                        'Actual': new_actual
                    }
                ])

                st.session_state.fleet_data = pd.concat(
                    [
                        st.session_state.fleet_data,
                        new_row
                    ],
                    ignore_index=True
                )

                st.success("Truck added successfully.")

                st.rerun()

    # DELETE TRUCK
    with col2:

        st.subheader("Delete Truck")

        delete_target = st.selectbox(
            "Select Truck ID",
            merged_data['Truck_ID'].unique()
        )

        if st.button("DELETE TRUCK"):

            st.session_state.fleet_data = st.session_state.fleet_data[
                st.session_state.fleet_data['Truck_ID'] != delete_target
            ]

            st.warning(f"{delete_target} deleted.")

            st.rerun()

# --- 8. AUDITS ---
elif page == "Audits":

    st.header("Operational Integrity Log")

    for _, row in merged_data.iterrows():

        is_ontime = row['Actual'] <= row['ETD']

        status_text = "ON TIME" if is_ontime else "DELAYED"

        status_color = "#22c55e" if is_ontime else "#ef4444"

        st.markdown(
            f"""
            <div class="audit-box">
            [NODE_LOG]: {row['Truck_ID']} |
            OP: {row['Driver']}
            <br>
            ROUTE: {row['Route']}
            <br>
            STATUS:
            <span style="color:{status_color}; font-weight:bold;">
            {status_text}
            </span>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- 9. ANALYTICS ---
elif page == "Analytics":

    st.header("Fleet Intelligence")

    r1c1, r1c2, r1c3 = st.columns(3)

    avg_fuel = st.session_state.fleet_data['Fuel'].mean()

    gauge_fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=avg_fuel,
            title={'text': "Avg Fuel %"},
            gauge={
                'bar': {
                    'color': "#f97316"
                }
            }
        )
    )

    gauge_fig.update_layout(height=300)

    r1c1.plotly_chart(
        gauge_fig,
        use_container_width=True
    )

    pie_fig = px.pie(
        merged_data,
        names='Status',
        color_discrete_sequence=['#f97316', '#0f172a']
    )

    pie_fig.update_layout(title="Asset Status")

    r1c2.plotly_chart(
        pie_fig,
        use_container_width=True
    )

    bar_fig = px.bar(
        merged_data,
        x='City',
        title="Units per Hub",
        color_discrete_sequence=['#f97316']
    )

    bar_fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)"
    )

    r1c3.plotly_chart(
        bar_fig,
        use_container_width=True
    )

    r2c1, r2c2, r2c3 = st.columns(3)

    delays = len(
        merged_data[
            merged_data['Actual'] > merged_data['ETD']
        ]
    )

    maintenance = len(
        merged_data[
            merged_data['Status'] == 'Maintenance'
        ]
    )

    active_regions = len(
        merged_data['City'].unique()
    )

    r2c1.metric("Delayed Arrivals", delays)
    r2c2.metric("In Maintenance", maintenance)
    r2c3.metric("Active Regions", active_regions)

# --- 10. FOOTER ---
st.divider()

st.caption("OMNI Logistics Dashboard © 2026")