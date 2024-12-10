from fastapi import APIRouter, Depends
from src.common.utils import responseFormatter
from ..schemas.index import (
    UsuarioLoginSchema,
    UsuarioUpdateSchema,
    UsuarioChangePasswordSchema,
)
from ..services import authentication, usuario
from src.application.autentificacion.middleware.jwtValidator import JWTBearer

router = APIRouter()


@router.post("/auth")
async def authUser(userLogin: UsuarioLoginSchema):
    response = authentication.loginUsuario(userLogin.usuario, userLogin.contrasenia)
    return responseFormatter.successResponse(
        data=response, message="Autentificacion exitosa"
    )


@router.get("/perfil/{id}", dependencies=[Depends(JWTBearer())])
async def getPerfil(id: int):
    response = usuario.getUsuarioService(id)
    return responseFormatter.successResponse(
        data=response, message="Perfil usuario existosa"
    )


@router.patch("/usuarios/{id}", dependencies=[Depends(JWTBearer())])
async def createDocumento(id: int, user: UsuarioUpdateSchema):
    response = usuario.updateUserService(id, user)
    return responseFormatter.successResponse(
        data=response, message="Usuario actualizado correctamente"
    )


@router.patch("/usuarios/{id}/contrasenia", dependencies=[Depends(JWTBearer())])
async def createDocumento(id: int, userChangePassword: UsuarioChangePasswordSchema):
    response = usuario.updatePassword(
        id, userChangePassword.oldPassword, userChangePassword.newPassword
    )
    return responseFormatter.successResponse(
        data=response, message="Contraseña actualizado correctamente"
    )
