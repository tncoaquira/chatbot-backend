from src.database.chatbotDB import db
from src.application.autentificacion.models.index import Usuario
from ..models.index import Usuario

def obtenerUsuarioPorUsername(username: str):
    db.rollback()
    query = db.query(Usuario).filter(Usuario.usuario == username)
    usuario = query.one_or_none()
    return usuario

def getUserById(idUser: int):
    db.rollback()
    query = db.query(Usuario).filter(Usuario.id == idUser)
    usuario = query.one_or_none()
    return usuario

def updateUser(user: Usuario, userUpdate: dict):
    for key, value in userUpdate.items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user