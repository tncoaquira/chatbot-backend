from fastapi import APIRouter, Query, Depends
from ..services import documentos
from src.common.utils import responseFormatter
from src.application.autentificacion.middleware.jwtValidator import JWTBearer
from ..schemas.index import DocumentoCrear, DocumentoUpdate

router = APIRouter()


@router.get("/documentos", dependencies=[Depends(JWTBearer())])
async def getDocumentos(
    pagina: str = Query(1, alias="pagina"), filtro: str = Query(None, alias="filtro")
):
    response = documentos.getDocumentosService(pagina, filtro)
    return responseFormatter.successResponse(response)


@router.get("/documentos/{id}/preguntas",dependencies=[Depends(JWTBearer())])
async def getDocumentos(id: int):
    response = documentos.getPreguntasPorDocumentoService(id)
    return responseFormatter.successResponse(response)


@router.post("/documentos", dependencies=[Depends(JWTBearer())])
async def createDocumento(documento: DocumentoCrear):
    response = documentos.createDocumentoService(documento)
    return responseFormatter.successResponse(data=response, message="Creado Exitosamente")


@router.patch("/documentos/{id}", dependencies=[Depends(JWTBearer())])
async def createDocumento(id: int, documento: DocumentoUpdate):
    response = documentos.updateDocumentoService(id, documento)
    return responseFormatter.successResponse(
        data=response, message="Actualizado correctamente"
    )


@router.patch("/documentos/{id}/activar", dependencies=[Depends(JWTBearer())])
async def activarDocumento(id: int):
    response = documentos.activarDocumentoService(id)
    return responseFormatter.successResponse(
        data=response, message="Activado correctamente"
    )


@router.patch("/documentos/{id}/inactivar", dependencies=[Depends(JWTBearer())])
async def inactivarDocumento(id: int):
    response = documentos.inactivarDocumentoService(id)
    return responseFormatter.successResponse(
        data=response, message="Inactivado correctamente"
    )
