from sqlalchemy.orm import Session
from fastapi import Request
from typing import Optional
from datetime import datetime

from models.AuditLogs import AuditLog


def log_audit(
    db: Session,
    *,
    actor_id: Optional[int],
    actor_role: str,
    action: str,
    entity_type: str,
    entity_id: Optional[int],
    old_value: Optional[dict],
    new_value: Optional[dict],
    request: Request
) -> None:
    """
    Create an audit log entry.

    This function must NEVER raise an exception that breaks the main flow.
    Audit failure should not stop business logic.
    """

    try:
        ip_address = (
            request.client.host
            if request.client
            else "UNKNOWN"
        )

        user_agent = request.headers.get("user-agent")

        audit = AuditLog(
            actor_id=actor_id,
            actor_role=actor_role,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.utcnow()
        )

        db.add(audit)
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"[AUDIT LOG ERROR] {str(e)}")
