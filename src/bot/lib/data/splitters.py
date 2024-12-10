import logging
from src.bot.constante.index import NRO_SUPERPOSICION, NRO_TOKEN_MODELO, CODIFICADOR_TOKEN
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
    Language,
)
from langchain.schema import Document
import tiktoken

logger = logging.getLogger(__name__)

def splitDocumentos(documentos):
    docs_split_by_heders = []
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
    ]
    method_headers_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
    method_recursive_text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN,
        chunk_size=NRO_TOKEN_MODELO,
        chunk_overlap=NRO_SUPERPOSICION,
        length_function=countTokens,
    )

    try:
        for doc in documentos:
            docs_split = method_headers_splitter.split_text(doc.page_content)
            docs_split = method_recursive_text_splitter.split_documents(docs_split)
            docs_split_result = [
                Document(
                    page_content=doc_split.page_content,
                    metadata={**doc_split.metadata, **doc.metadata},
                )
                for doc_split in docs_split
            ]
            docs_split_by_heders.extend(docs_split_result)
        logger.info(f"Division de documentos terminada con exito")
        data = {"totalDocs": len(docs_split_by_heders), "docs": docs_split_by_heders}
        return data
    except Exception as e:
        logger.error(f"Error al dividir los documentos: {e}")


def countTokens(texto):
    encoding = tiktoken.get_encoding(CODIFICADOR_TOKEN)
    tokens = encoding.encode(texto)
    return len(tokens)
