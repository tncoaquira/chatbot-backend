from ..repositories import usuarios
from datetime import datetime, timedelta, timezone
import jwt
from src.config.chatbot import Config
from fastapi import HTTPException, status
from src.common.utils import bcrypt
from ..schemas.index import UsuarioPerfilSchema


def authenticateUser(username: str, password: str):
    usuario = usuarios.obtenerUsuarioPorUsername(username=username)
    if not usuario:
        return False
    if not bcrypt.verifyPassword(password, usuario.contrasenia):
        return False
    return usuario


def createAccessToken(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=4 * 60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


def loginUsuario(username, password):
    usuario = authenticateUser(username, password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El nombre de usuario o contraseña es incorrecta",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = createAccessToken(
        data={"sub": str(usuario.id)}, expires_delta=access_token_expires
    )
    userPerfil = UsuarioPerfilSchema(
        id=usuario.id,
        usuario=usuario.usuario,
        correo=usuario.correo,
        nombres=usuario.nombres,
        apellidos=usuario.apellidos,
        ci=usuario.ci,
    )
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "user": userPerfil.dict(exclude_unset=True),
    }
