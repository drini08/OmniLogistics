import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.driver import Driver, DriverCreate, DriverResponse
from database import get_db_connection
from auth.security import get_api_key

router = APIRouter()


@router.get("/", response_model=List[DriverResponse])
def get_drivers(current_user: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, license_category, contact_number, is_active FROM drivers")
    drivers = cursor.fetchall()
    conn.close()
    return [
        {
            "id": driver[0],
            "full_name": driver[1],
            "license_category": driver[2],
            "contact_number": driver[3],
            "is_active": bool(driver[4])
        } for driver in drivers
    ]


@router.post("/", response_model=DriverResponse)
def create_driver(
        driver: DriverCreate,
        current_user: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO drivers (full_name, license_category, contact_number, password, is_active) VALUES (?, ?, ?, ?, ?)",
            (driver.full_name, driver.license_category, driver.contact_number, driver.password, driver.is_active)
        )
        conn.commit()
        driver_id = cursor.lastrowid
        return DriverResponse(id=driver_id, **driver.dict())
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Driver registration failed. Contact number may already exist."
        )
    finally:
        conn.close()


@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(
        driver_id: int,
        driver: DriverCreate,
        current_user: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE drivers SET full_name = ?, license_category = ?, contact_number = ?, is_active = ? WHERE id = ?",
        (driver.full_name, driver.license_category, driver.contact_number, driver.is_active, driver_id)
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Driver not found")

    conn.commit()
    conn.close()
    return DriverResponse(id=driver_id, **driver.dict())


@router.delete("/{driver_id}", response_model=dict)
def delete_driver(
        driver_id: int,
        current_user: str = Depends(get_api_key)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM drivers WHERE id = ?", (driver_id,))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Driver not found")

    conn.commit()
    conn.close()
    return {"detail": "Driver removed from OmniLogistics records"}