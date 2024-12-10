from src.database.chatbotDB import db
from src.application.baseConocimiento.models.index import Documento
from src.application.baseConocimiento.models.index import Pregunta
from sqlalchemy import select, func, or_
from ..schemas.index import DocumentoUpdate


def getDocumentosPaginado(pagina: int = 1, filtro: str = None):

    db.rollback()
    query = db.query(Documento)
    if filtro:
        query = query.where(
            or_(
                Documento.titulo.like(f"%{filtro}%"),
                Documento.contenido.like(f"%{filtro}%"),
                Documento.link.like(f"%{filtro}%"),
                Documento.palabrasClave.like(f"%{filtro}%"),
                Documento.topics.like(f"%{filtro}%"),
            )
        )

    if pagina and int(pagina) > 0:
        query = query.offset(((int(pagina)) - 1) * 10)

    """ query_conteo = db.query(Pregunta).filter(query.statement) """  # TODO: corregir el contador
    conteo = query.count()

    query = query.limit(10)

    documentos = query.all()

    return {
        "filas": [
            {
                "id": row.id,
                "titulo": row.titulo,
                "contenido": row.contenido,
                "link": row.link,
                "metadata_documento": row.metadata_documento,
                "palabrasClave": row.palabrasClave,
                "topics": row.topics,
                "_status": row._status,
            }
            for row in documentos
        ],
        "total": conteo,
    }


def createDocumento(documento: Documento):
    db.rollback()
    db.add(documento)
    db.commit()
    db.refresh(documento)
    return documento


def getDocumentoPorId(idDocumento: int):
    db.rollback()
    query = db.query(Documento).filter(Documento.id == idDocumento)
    documento = query.one_or_none()
    return documento


def updateDocumento(documento: Documento, documentoUpdate: dict):
    for key, value in documentoUpdate.items():
        if hasattr(documento, key):
            setattr(documento, key, value)
    db.commit()
    db.refresh(documento)
    return documento
