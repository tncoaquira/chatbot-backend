from ..repositories.conocimiento import getDocumentosEstructurados
import logging
from langchain.schema import Document
import textwrap


logger = logging.getLogger(__name__)
from src.bot.lib.memory import ingesta


def getDocumentosEstructuradosService():
    documentos = getDocumentosEstructurados()
    try:
        documentos_formateados = [
            Document(
                page_content=textwrap.dedent(
                    f"""# {doc["titulo"]}
            ---

            ## Palabras Clave
            - {doc["palabrasClave"]}

            ## Contenido del Documento
            {doc["contenido"]}

            ## Enlaces Relacionados
            {"\n".join(f"- [Enlace]({link})" for link in doc['link'].split(','))}

            ---

            **Importante:** Este documento resuelve las siguientes preguntas:  
            {"\n".join(f"- {preg}" for preg in doc['preguntas'])}
            """
                ),
                metadata={
                    "content_type": "text",
                    "charset": "UTF-8",
                    "title": str(doc["titulo"]),
                    "keywords": str(doc["palabrasClave"]),
                    "enlaces": str(doc["link"]),
                    "topics": str(doc["topics"]),
                    "detalles": str(doc["metadata_documento"]),
                    "preguntas_asociadas": ",".join(
                        f"- {preg}" for preg in doc["preguntas"]
                    ),
                    "source": f"documento-db-{str(doc["id"])}",
                },
            )
            for doc in documentos
        ]
        return documentos_formateados
    except Exception as e:
        logger.error(f"Error al contruir los documentos DB: {e} ")
        return []

