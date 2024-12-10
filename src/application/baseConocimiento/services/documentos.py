from ..repositories import documentos
from ..services import preguntas
from ..schemas.index import DocumentoCrear, DocumentoUpdate
from src.common.utils import responseFormatter
from ..models.index import Documento

import logging

logger = logging.getLogger(__name__)


def getDocumentosService(pagina, filtro):
    documentosResultado = documentos.getDocumentosPaginado(pagina, filtro)
    return documentosResultado


def buscarDocumentoPorIdService(idDocumento):
    resultado = documentos.getDocumentoPorId(idDocumento)
    return resultado


def getPreguntasPorDocumentoService(idDocument: int):
    documento = buscarDocumentoPorIdService(idDocument)
    if documento is None:
        return responseFormatter.errorResponse(
            detail="", message="El documento no existe", status_code=400
        )
    resultado = preguntas.getPreguntasPorDocumentoService(idDocument)
    return resultado


def createDocumentoService(documento: DocumentoCrear):
    if documento is None:
        return responseFormatter.errorResponse(
            detail="", message="El documento a crear esta vacio", status_code=400
        )
    try:
        documentoNuevo = Documento(
            titulo=documento.titulo,
            contenido=documento.contenido,
            link=documento.link,
            palabrasClave=documento.palabrasClave,
            metadata_documento=documento.link,
            topics=documento.topics,
        )
        documento = documentos.createDocumento(documentoNuevo)
        return {"id": documento.id}
    except Exception as e:
        logger.error(e)
        responseFormatter.errorResponse(
            detail=e, message="Ocurrio un error al crear", status_code=500
        )


def updateDocumentoService(idDocumento: int, documentoUpdate: DocumentoUpdate):
    documento = buscarDocumentoPorIdService(idDocumento)
    if documento is None:
        return responseFormatter.errorResponse(
            detail="", message="El documento no existe", status_code=400
        )
    try:
        documentoUpdateDic = documentoUpdate.model_dump(exclude_unset=True)
        documentoActualizado = documentos.updateDocumento(documento, documentoUpdateDic)
        print("documentoActualizado__________________________")
        print(documentoActualizado)
        return {"id": documentoActualizado.id}
    except Exception as e:
        logger.error(e)
        responseFormatter.errorResponse(
            detail=e, message="Ocurrio un error al crear", status_code=500
        )


def activarDocumentoService(idDocumento: int):
    documento = buscarDocumentoPorIdService(idDocumento)
    if documento is None:
        return responseFormatter.errorResponse(
            detail="", message="El documento no existe", status_code=400
        )
    try:
        documentoUpdateDic = {"_status": "ACTIVO"}
        documentoActualizado = documentos.updateDocumento(documento, documentoUpdateDic)
        return {"id": documentoActualizado.id}
    except Exception as e:
        logger.error(e)
        responseFormatter.errorResponse(
            detail=e, message="Ocurrio un error al crear", status_code=500
        )


def inactivarDocumentoService(idDocumento: int):
    documento = buscarDocumentoPorIdService(idDocumento)
    if documento is None:
        return responseFormatter.errorResponse(
            detail="", message="El documento no existe", status_code=400
        )
    try:
        documentoUpdateDic = {"_status": "INACTIVO"}
        documentoActualizado = documentos.updateDocumento(documento, documentoUpdateDic)
        return {"id": documentoActualizado.id}
    except Exception as e:
        logger.error(e)
        responseFormatter.errorResponse(
            detail=e, message="Ocurrio un error al crear", status_code=500
        )
