from ..repositories import preguntas
from src.common.utils import responseFormatter
from ..schemas.index import PreguntaUpdate
from ..models.index import Pregunta


def getPreguntasService(pagina, filtro, activos):
    resultado = preguntas.getPreguntasPaginado(pagina, filtro, activos)
    return resultado


def getPreguntaPorIdService(idPregunta):
    resultado = preguntas.getPreguntaPorId(idPregunta)
    return resultado


def updatePregunta(idPregunta: int, preguntaUpdate: PreguntaUpdate):
    pregunta = getPreguntaPorIdService(int(idPregunta))
    if pregunta is None:
        return responseFormatter.errorResponse(
            detail="", message="la pregunta no existe", status_code=400
        )

    resultado = preguntas.updatePregunta(pregunta, preguntaUpdate)
    return resultado


def getPreguntasPorDocumentoService(idDocumento: int):
    resultado = preguntas.getPreguntasPorDocumento(idDocumento)
    return resultado


def createPreguntaService(pregunta: Pregunta):
    if pregunta is None:
        return responseFormatter.errorResponse(
            detail="", message="La pregunta a crear esta vacia", status_code=400
        )
    try:
        preguntaNueva = Pregunta(
            textoPregunta=pregunta.textoPregunta, idDocumento=pregunta.idDocumento
        )
        resultado = preguntas.createPregunta(preguntaNueva)
        return {"id": resultado.id}
    except Exception as e:
        responseFormatter.errorResponse(
            detail=e, message="Ocurrio un error al crear", status_code=500
        )


def updatePreguntaService(idPregunta: int, preguntaUpdate: PreguntaUpdate):
    pregunta = getPreguntaPorIdService(idPregunta)
    if pregunta is None:
        return responseFormatter.errorResponse(
            detail="", message="La pregunta no existe", status_code=400
        )
    try:
        preguntaUpdateDic = preguntaUpdate.model_dump(exclude_unset=True)
        documentoActualizado = preguntas.updatePregunta(pregunta, preguntaUpdateDic)
        return {"id": documentoActualizado.id}
    except Exception as e:
        responseFormatter.errorResponse(
            detail=e, message="Ocurrio un error al crear", status_code=500
        )


def inactivarPreguntaService(idPregunta: int):
    pregunta = getPreguntaPorIdService(idPregunta)
    if pregunta is None:
        return responseFormatter.errorResponse(
            detail="", message="El pregunta no existe", status_code=400
        )
    try:
        preguntaUpdateDic = {"_status": "INACTIVO"}
        documentoActualizado = preguntas.updatePregunta(pregunta, preguntaUpdateDic)
        return {"id": documentoActualizado.id}
    except Exception as e:
        responseFormatter.errorResponse(
            detail=e,
            message="Ocurrio un error al inactivar la pregunta",
            status_code=500,
        )


def activarPreguntaService(idPregunta: int):
    pregunta = getPreguntaPorIdService(idPregunta)
    if pregunta is None:
        return responseFormatter.errorResponse(
            detail="", message="El pregunta no existe", status_code=400
        )
    try:
        preguntaUpdateDic = {"_status": "ACTIVO"}
        documentoActualizado = preguntas.updatePregunta(pregunta, preguntaUpdateDic)
        return {"id": documentoActualizado.id}
    except Exception as e:
        responseFormatter.errorResponse(
            detail=e,
            message="Ocurrio un error al activar la pregunta",
            status_code=500,
        )
