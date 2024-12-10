from fastapi import APIRouter, Depends, Query
from ..services import preguntas
from src.common.utils import responseFormatter
from ..schemas.index import PreguntaUpdate, PreguntaCrear
from src.application.autentificacion.middleware.jwtValidator import JWTBearer

router = APIRouter()


@router.get("/preguntas", dependencies=[Depends(JWTBearer())])
async def getPreguntas(
    pagina: str = Query(1, alias="pagina"),
    filtro: str = Query(None, alias="filtro"),
    activos: bool = Query(None, alias="activos"),
):
    response = preguntas.getPreguntasService(pagina, filtro, activos)
    return responseFormatter.successResponse(response)


@router.post("/preguntas", dependencies=[Depends(JWTBearer())])
async def createPregunta(pregunta: PreguntaCrear):
    response = preguntas.createPreguntaService(pregunta)
    return responseFormatter.successResponse(
        data=response, message="Creado correctamente"
    )


@router.patch("/preguntas/{id}", dependencies=[Depends(JWTBearer())])
async def updatePregunta(id: int, pregunta: PreguntaUpdate):
    response = preguntas.updatePreguntaService(id, pregunta)
    return responseFormatter.successResponse(
        data=response, message="Actualizado correctamente"
    )


@router.patch("/preguntas/{id}/activar", dependencies=[Depends(JWTBearer())])
async def updatePregunta(id: int):
    response = preguntas.activarPreguntaService(id)
    return responseFormatter.successResponse(
        data=response, message="Actualizado correctamente"
    )


@router.patch("/preguntas/{id}/inactivar", dependencies=[Depends(JWTBearer())])
async def updatePregunta(id: int):
    response = preguntas.inactivarPreguntaService(id)
    return responseFormatter.successResponse(
        data=response, message="Actualizado correctamente"
    )
