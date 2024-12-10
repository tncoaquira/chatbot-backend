from fastapi import APIRouter, Depends
from ..services import sincronizacion
from src.common.utils import responseFormatter
from src.application.autentificacion.middleware.jwtValidator import JWTBearer

router = APIRouter()


@router.get("/sincronizacion/basedatos", dependencies=[Depends(JWTBearer())])
async def sincronizarDatabase():
    sincronizacion.sincronizarDatabaseService()
    return responseFormatter.successResponse(
        data="", message="Sincronizado exitozamente"
    )
