from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func
from src.database.chatbotDB import Base


class AuditoriaBase(Base):
    __abstract__ = True

    _created_at = Column(DateTime, default=func.now())
    _updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    _created_by = Column(Integer)
    _updated_by = Column(Integer)
    _status = Column(String, default="ACTIVO")
