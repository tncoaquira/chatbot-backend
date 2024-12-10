from ..schemas.index import UsuarioUpdateSchema, UsuarioPerfilSchema
from ..repositories import usuarios
from src.common.utils import responseFormatter
from fastapi import HTTPException
import logging
from src.common.utils import bcrypt
from ..models.index import Usuario

logger = logging.getLogger(__name__)


def getUsuarioService(idUser: int):
    user = usuarios.getUserById(idUser)
    return {
        "id": user.id,
        "usuario": user.usuario,
        "nombres": user.nombres,
        "apellidos": user.apellidos,
        "ci": user.ci,
        "correo": user.correo,
    }


def updateUserService(idUser: int, userUpdate: UsuarioUpdateSchema):
    user = usuarios.getUserById(idUser)
    if user is None:
        return responseFormatter.errorResponse(
            detail="", message="El usuario no se encotro", status_code=400
        )
    try:
        userUpdateDic = userUpdate.model_dump(exclude_unset=True)
        userUpdated = usuarios.updateUser(user, userUpdateDic)
        return {"id": userUpdated.id}
    except Exception as e:
        logger.error(e)
        responseFormatter.errorResponse(
            detail=e, message="Ocurrio un error actualizar al usuario", status_code=500
        )


def updatePassword(idUser: str, oldPassword: str, newPassword: str):
    user = usuarios.getUserById(idUser)
    if user is None:
        raise HTTPException(status_code=403, detail="Usuario inexistente")

    validatePassword = bcrypt.verifyPassword(oldPassword, user.contrasenia)
    if not validatePassword:
        raise HTTPException(status_code=403, detail="Contraseña antigua incorrecta")

    hashNewPassword = bcrypt.getHashPassword(newPassword)
    usuarioDic = {"contrasenia": hashNewPassword}
    userUpdated = usuarios.updateUser(user, usuarioDic)
    return {"id": userUpdated.id}
