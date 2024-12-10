from sqlalchemy import Column, String, Integer, ForeignKey
from src.common.models.auditoriaBase import AuditoriaBase
from sqlalchemy.orm import relationship


class Documento(AuditoriaBase):
    __tablename__ = "documentos"
    __table_args__ = {"schema": "conocimiento"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String)
    contenido = Column(String)
    link = Column(String, nullable=True)
    metadata_documento = Column(String, nullable=True)
    palabrasClave = Column(String, name="palabras_clave")
    topics=Column(String, nullable=True)
    preguntas = relationship("Pregunta", back_populates="documentos")
    

class Pregunta(AuditoriaBase):
    __tablename__ = "preguntas"
    __table_args__ = {"schema": "conocimiento"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    textoPregunta = Column(String, name="texto_pregunta")
    idDocumento = Column(
        Integer, ForeignKey("conocimiento.documentos.id"), name="id_documento"
    )
    documentos = relationship("Documento", back_populates="preguntas")



