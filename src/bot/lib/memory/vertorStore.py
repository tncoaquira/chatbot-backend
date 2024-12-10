from langchain_chroma import Chroma
from langchain.indexes import SQLRecordManager, index
import logging
from src.common.baseSingleton import SingletonBase
from langchain.schema import Document

logger = logging.getLogger(__name__)


class VectorMemory(SingletonBase):
    def __init__(
        self,
        chroma_collection_name,
        chroma_persist_dir,
        sqlRecord_db_url,
        embedding,
    ) -> None:
        super().__init__()
        self.chroma_collection_name = chroma_collection_name
        self.embedding = embedding
        self.vector_store = self.loadMemoryIndex(
            chroma_collection_name, chroma_persist_dir
        )
        self.record_manager = self.loadSQLRecordManager(sqlRecord_db_url)

    def getVectorStore(self):
        return self.vector_store

    def loadMemoryIndex(self, chroma_collection_name, chroma_persist_dir):
        try:
            vector_store = Chroma(
                collection_name=str(chroma_collection_name),
                embedding_function=self.embedding,
                persist_directory=chroma_persist_dir,
            )
            logger.info(f"se inicio un vector store de nombre {chroma_collection_name}")
        except Exception as e:
            logger.error(f"Error inesperado al iniciar chroma, descripcion: {e}")
        return vector_store

    def loadSQLRecordManager(self, sqlRecord_db_url):
        NAMESPACE = f"chroma/{self.chroma_collection_name}"
        try:
            record_manager = SQLRecordManager(
                namespace=NAMESPACE, db_url=sqlRecord_db_url
            )
            record_manager.create_schema()
            logger.info(
                f"se inicio el record manager para chroma: {self.chroma_collection_name}"
            )
        except Exception as e:
            logger.error(
                f"Error inesperado al iniciar record manager, descripcion: {e}"
            )
        return record_manager

    def clear(self):
        index(
            [],
            self.record_manager,
            self.vector_store,
            cleanup="full",
            source_id_key="source",
        )
        logger.info("Índice limpiado con éxito, vector store vacia.")

    def clearDataFull(self, docs):
        result_index = index(
            docs,
            self.record_manager,
            self.vector_store,
            cleanup="full",
            source_id_key="source",
        )
        logger.info(
            f"Índice limpiado con éxito, sin duplicados y actualizad. Resultado: {result_index}"
        )

    def clearDataIncremental(self, docs):
        result_index = index(
            docs,
            self.record_manager,
            self.vector_store,
            cleanup="incremental",
            source_id_key="source",
        )
        logger.info(
            f"Índice limpiado con éxito, actualizado registros que han cambiado o nuevos. Resultado: {result_index}"
        )

    def getDocuments(self):
        documentos = self.vector_store.get(
            ids=self.record_manager.list_keys(), include=["documents", "metadatas"]
        )
        docs = [
            Document(page_content=page_content, metadata=metadata)
            for page_content, metadata in zip(
                documentos["documents"], documentos["metadatas"]
            )
        ]
        if len(docs) > 0:
            return docs
        docs = [Document(page_content="empty", metadata={"source": "empty"})]
        return docs

    def existsDocuments(self):
        documentos = self.vector_store.get(
            ids=self.record_manager.list_keys(), include=["documents", "metadatas"]
        )
        if len(documentos) ==0:
            return False
        return True
