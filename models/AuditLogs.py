# Imports
from sqlalchemy import Column, Integer , ForeignKey , String , DateTime , JSON
from database import Base
from sqlalchemy.sql import func

# Definition
class AuditLogs(Base):
    __tablename__="audit_logs"
    id = Column(Integer , primary_key=True , index=True)
    actor_id = Column(Integer , ForeignKey("users.id"))
    actor_role = Column(String, nullable=False)
    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)

    old_value = Column(JSON)
    new_value = Column(JSON)

    ip_address = Column(String)
    user_agent = Column(String)

    created_at = Column(DateTime, default=func.now())