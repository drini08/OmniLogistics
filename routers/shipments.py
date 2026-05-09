import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.shipment import ShipmentCreate, ShipmentResponse, ShipmentUpdate
from database import get_db_connection
from auth.security import get_api_key

router = APIRouter()


@router.get("/", response_model=List[ShipmentResponse])
def get_shipments(current_user: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, origin, destination, cargo_weight, 
               truck_id, driver_id, status 
        FROM shipments
    """)

    shipments = cursor.fetchall()
    conn.close()

    return [
        {
            "id": shipment[0],
            "origin": shipment[1],
            "destination": shipment[2],
            "cargo_weight": shipment[3],
            "truck_id": shipment[4],
            "driver_id": shipment[5],
            "status": shipment[6]
        } for shipment in shipments
    ]


@router.post("/", response_model=ShipmentResponse)
def create_shipment(
        shipment: ShipmentCreate,
        current_user: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("SELECT max_load_capacity, status FROM trucks WHERE id = ?", (shipment.truck_id,))
        truck = cursor.fetchone()

        if not truck:
            raise HTTPException(status_code=404, detail="Assigned truck not found.")
        if truck["status"] != "Healthy":
            raise HTTPException(status_code=400, detail="Cannot assign shipment to a truck requiring maintenance.")
        if shipment.cargo_weight > truck["max_load_capacity"]:
            raise HTTPException(
                status_code=400,
                detail=f"Weight Validation Failed: Cargo ({shipment.cargo_weight}t) exceeds truck capacity ({truck['max_load_capacity']}t)."
            )





        cursor.execute("SELECT is_active FROM drivers WHERE id = ?", (shipment.driver_id,))
        driver = cursor.fetchone()
        if not driver or not driver["is_active"]:
            raise HTTPException(status_code=400, detail="Assigned driver is not active or not found.")


        cursor.execute("""
            INSERT INTO shipments (origin, destination, cargo_weight, truck_id, driver_id, status)
            VALUES (?, ?, ?, ?, ?, 'Scheduled')
        """, (shipment.origin, shipment.destination, shipment.cargo_weight, shipment.truck_id, shipment.driver_id))

        shipment_id = cursor.lastrowid


        cursor.execute("""
            INSERT INTO audit_log (actor_id, action_type, affected_entity, after_value)
            VALUES (?, 'CREATE_SHIPMENT', 'Shipment', ?)
        """, (current_user, f"Shipment {shipment_id} to {shipment.destination}"))

        conn.commit()
        return ShipmentResponse(id=shipment_id, status="Scheduled", **shipment.dict())

    finally:
        conn.close()






@router.put("/{shipment_id}/status", response_model=dict)
def update_shipment_status(
        shipment_id: int,
        new_status: str,
        current_user: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute("SELECT status FROM shipments WHERE id = ?", (shipment_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Shipment not found")

    old_status = row["status"]

    cursor.execute("UPDATE shipments SET status = ? WHERE id = ?", (new_status, shipment_id))


    cursor.execute("""
        INSERT INTO audit_log (actor_id, action_type, affected_entity, before_value, after_value)
        VALUES (?, 'UPDATE_STATUS', 'Shipment', ?, ?)
    """, (current_user, old_status, new_status))

    conn.commit()
    conn.close()

    return {"id": shipment_id, "status": new_status, "detail": "Status updated successfully"}