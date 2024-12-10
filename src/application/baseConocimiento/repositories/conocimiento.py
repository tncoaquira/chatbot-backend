from src.database.chatbotDB import db
from src.application.baseConocimiento.models.index import Documento
from src.application.baseConocimiento.models.index import Pregunta
from sqlalchemy import select, func


def getDocumentosEstructurados():
    stmt = (
        select(
            Documento.id,
            Documento.titulo,
            Documento.contenido,
            Documento.link,
            Documento.metadata_documento,
            Documento.palabrasClave,
            Documento.topics,
            func.array_agg(
                func.distinct(
                    Pregunta.textoPregunta,
                )
            ).label("preguntas")
        )
        .join(Pregunta, Documento.id == Pregunta.idDocumento)
        .group_by(Documento.id)
    )

    result = db.execute(stmt)

    documentosEstructurados = [
        {
            "id": row.id,
            "titulo": row.titulo,
            "contenido": row.contenido,
            "link": row.link,
            "topics": row.topics,
            "metadata_documento": row.metadata_documento,
            "palabrasClave": row.palabrasClave,
            "preguntas": row.preguntas,
        }
        for row in result
    ]

    return documentosEstructurados
