from fastapi import APIRouter, Depends
from typing import List
from database import get_db_connection
from auth.security import get_api_key
from models.audit import AuditResponse # This matches your AuditResponse class

router = APIRouter()

@router.get("/", response_model=List[AuditResponse])
def get_all_logs(api_key: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # We select the columns to match your AuditBase fields
        cursor.execute("""
            SELECT id, timestamp, actor_id, action_type, 
                   affected_entity, before_value, after_value 
            FROM audit_logs 
            ORDER BY timestamp DESC
        """)
        logs = cursor.fetchall()
        
        # Mapping the database rows to your AuditResponse schema
        return [
            {
                "id": log[0],
                "timestamp": log[1],
                "actor_id": log[2],
                "action_type": log[3],
                "affected_entity": log[4],
                "before_value": log[5],
                "after_value": log[6]
            } for log in logs
        ]
    except Exception:
        return []
    finally:
        conn.close()