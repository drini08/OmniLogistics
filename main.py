from fastapi import FastAPI
from models import audit
from routers import trucks, drivers, shipments, audits, api_key
from database import create_database

app = FastAPI()

@app.on_event("startup")
def startup():
    create_database()

# The finished modules
app.include_router(api_key.router, prefix="/auth")
app.include_router(trucks.router, prefix="/trucks")
app.include_router(drivers.router, prefix="/drivers")
app.include_router(shipments.router, prefix="/shipments")
app.include_router(audits.router, prefix="/audit", tags=["Audit Trail"])