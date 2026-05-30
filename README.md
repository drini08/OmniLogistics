# OmniLogistics (OMNI Balkan Hub)

OmniLogistics is a comprehensive logistics and fleet management platform tailored for the Balkan region. It provides real-time tracking, fleet management, and operational analytics through a powerful combination of a FastAPI backend and a Streamlit dashboard.

## 🚀 Features

- **Real-Time Fleet Tracking:** Live GPS tracking of trucks across the Balkans (Pristina, Belgrade, Skopje, Tirana, etc.).
- **Operations Control Center:** Interactive dashboard for monitoring active trucks, in-transit shipments, and critical alerts.
- **Shipment Management:** Track origins, destinations, cargo types, weights, and delivery statuses.
- **Driver Management:** Keep track of driver profiles, experience, safety scores, and contact information.
- **Maintenance Tracking:** Log and monitor truck maintenance history, costs, and upcoming service needs.
- **Audit Trail:** Comprehensive logging of system actions for accountability.

## 🛠️ Technology Stack

- **Backend:** FastAPI (Python)
- **Frontend / Dashboard:** Streamlit
- **Database:** SQLite (with `sqlite3`)
- **Data Manipulation & Visualization:** Pandas, Plotly Express, Plotly Graph Objects
- **Server:** Uvicorn

## 📂 Project Structure

- `main.py`: Entry point for the FastAPI backend application.
- `app.py`: Streamlit frontend application providing the Operations Control Center dashboard.
- `database.py`: SQLite database initialization and connection management (`logistics.db`).
- `requirements`: List of Python dependencies for the project.
- `models/`: Pydantic models for data validation and API schemas.
- `routers/`: FastAPI route handlers for different modules (`trucks`, `drivers`, `shipments`, `audits`, `auth`).
- `utils/`: Utility functions and helpers.
- `auth/`: Authentication and authorization logic.

## ⚙️ Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd OmniLogistics
   ```

2. **Install dependencies:**
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements
   ```

3. **Initialize the Database:**
   ```bash
   python database.py
   ```

4. **Run the FastAPI Backend:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Run the Streamlit Dashboard (in a separate terminal):**
   ```bash
   streamlit run app.py
   ```

