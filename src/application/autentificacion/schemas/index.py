from pydantic import BaseModel
from typing import Optional


class UsuarioPerfilSchema(BaseModel):
    id: Optional[int] = None
    usuario: str
    contrasenia:Optional[str] = None
    correo: str
    nombres: str
    apellidos: str
    ci: str


class UsuarioUpdateSchema(BaseModel):
    correo: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    ci: Optional[str] = None


class UsuarioLoginSchema(BaseModel):
    usuario: str
    contrasenia: str

class UsuarioChangePasswordSchema(BaseModel):
    oldPassword: str
    newPassword: str