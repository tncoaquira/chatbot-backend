from sqlalchemy import Column, String, Integer
from src.common.models.auditoriaBase import AuditoriaBase

class Usuario(AuditoriaBase):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "autentificacion"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario = Column(String)
    contrasenia = Column(String)
    correo = Column(String)
    nombres = Column(String)
    apellidos = Column(String)
    ci=Column(String)
    




