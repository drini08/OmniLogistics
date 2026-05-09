import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.truck import Truck, TruckCreate, TruckResponse
from database import get_db_connection
from auth.security import get_api_key

router = APIRouter()

@router.get("/", response_model=List[TruckResponse])
def get_trucks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, license_plate, model_name, max_load_capacity, current_mileage, status FROM trucks")
    trucks = cursor.fetchall()
    conn.close()
    return [
        {
            "id": truck[0],
            "license_plate": truck[1],
            "model_name": truck[2],
            "max_load_capacity": truck[3],
            "current_mileage": truck[4],
            "status": truck[5]
        } for truck in trucks
    ]

@router.post("/", response_model=TruckResponse)
def create_truck(
    truck: TruckCreate,
    current_user: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO trucks (license_plate, model_name, max_load_capacity, current_mileage, status) VALUES (?, ?, ?, ?, ?)",
            (truck.license_plate, truck.model_name, truck.max_load_capacity, truck.current_mileage, "Healthy")
        )
        conn.commit()
        truck_id = cursor.lastrowid
        return TruckResponse(id=truck_id, status="Healthy", **truck.dict())
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Truck with plate '{truck.license_plate}' already exists."
        )
    finally:
        conn.close()


@router.put("/{truck_id}", response_model=TruckResponse)
def update_truck(
        truck_id: int,
        truck: TruckCreate,
        current_user: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        "UPDATE trucks SET license_plate = ?, model_name = ?, max_load_capacity = ?, current_mileage = ? WHERE id = ?",
        (truck.license_plate, truck.model_name, truck.max_load_capacity, truck.current_mileage, truck_id)
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Truck not found")

    conn.commit()
    conn.close()
    return TruckResponse(id=truck_id, status="Healthy", **truck.dict())


@router.delete("/{truck_id}", response_model=dict)
def delete_truck(
        truck_id: int,
        current_user: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute("DELETE FROM trucks WHERE id = ?", (truck_id,))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Truck not found")

    conn.commit()
    conn.close()

    return {"detail": "Truck removed from OmniLogistics fleet"}