from pydantic import BaseModel
from typing import Optional, List


class DocumentoCrear(BaseModel):
    titulo: str
    contenido: str
    link: str
    metadata_documento: str
    palabrasClave: str
    topics: str


class DocumentoUpdate(BaseModel):
    titulo: Optional[str] = None
    contenido: Optional[str] = None
    link: Optional[str] = None
    metadata_documento: Optional[str] = None
    palabrasClave: Optional[str] = None
    topics: Optional[str] = None


class PreguntaCrear(BaseModel):
    textoPregunta: str
    idDocumento: Optional[int] = None


class PreguntaUpdate(BaseModel):
    textoPregunta: Optional[str] = None
    idDocumento: Optional[int] = None
