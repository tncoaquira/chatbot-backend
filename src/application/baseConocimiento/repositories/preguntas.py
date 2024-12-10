from src.database.chatbotDB import db
from src.application.baseConocimiento.models.index import Pregunta
from ..schemas.index import PreguntaUpdate
from sqlalchemy import desc, asc


def getPreguntasPaginado(pagina: int = 1, filtro: str = None, activos=False):
    db.rollback()
    query = db.query(Pregunta)
    if filtro:
        query = query.where(Pregunta.textoPregunta.like(f"%{filtro}%"))

    if activos:
        query = query.where(Pregunta._status.like("ACTIVO"))

    """ query.order_by(Pregunta._updated_at) """# TODO: establecer 
    
    if pagina and int(pagina) > 0:
        query = query.offset(((int(pagina)) - 1) * 10)

    """ query_conteo = db.query(Pregunta).filter(query.statement) """  # TODO: corregir el contador
    conteo = query.count()

    query = query.limit(10)

    preguntas = query.all()

    return {
        "filas": [
            {
                "id": p.id,
                "textoPregunta": p.textoPregunta,
                "idDocumento": p.idDocumento,
                "_status": p._status,
            }
            for p in preguntas
        ],
        "total": conteo,
    }


def getPreguntasPorDocumento(idDocumento: int):
    db.rollback()
    query = db.query(Pregunta).filter(
        Pregunta.idDocumento == idDocumento, Pregunta._status == "ACTIVO"
    )
    preguntas = query.all()

    return {
        "filas": [{"id": p.id, "textoPregunta": p.textoPregunta} for p in preguntas]
    }


def getPreguntaPorId(idPregunta: int):
    db.rollback()
    query = db.query(Pregunta).filter(Pregunta.id == idPregunta)
    pregunta = query.one_or_none()
    return pregunta


def updatePregunta(pregunta: Pregunta, preguntaUpdateDics: dict):
    for key, value in preguntaUpdateDics.items():
        if hasattr(pregunta, key):
            setattr(pregunta, key, value)
    db.commit()
    db.refresh(pregunta)
    return pregunta


def createPregunta(pregunta: Pregunta):
    db.rollback()
    db.add(pregunta)
    db.commit()
    db.refresh(pregunta)
    return pregunta
