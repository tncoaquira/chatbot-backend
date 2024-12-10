from fastapi import APIRouter
from ..services import comunicacion
from src.common.utils import responseFormatter
from ..schemas.index import PreguntaBot

router = APIRouter()


@router.post("/comunicacion")
async def resolverPregunta(preguntaBot: PreguntaBot):
    response = comunicacion.resolverPreguntaService(preguntaBot)
    return responseFormatter.successResponse(response)


