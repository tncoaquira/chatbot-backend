from langchain.retrievers import EnsembleRetriever
from src.common.baseSingleton import SingletonBase
import logging
from langchain_community.document_transformers import LongContextReorder
from src.config.chatbot import Config


logger = logging.getLogger(__name__)


class RetriverModel(SingletonBase):

    def __init__(self, keyword_retriver, semantic_retriver):
        self.retriver = None
        self.configRetriver(keyword_retriver, semantic_retriver)

    def configRetriver(self, keyword_retriver, semantic_retriver):
        try:
            self.retriver = EnsembleRetriever(
                retrievers=[keyword_retriver, semantic_retriver],
                weights=[Config.WEIGHT_KEYWORD_RETRIVER, Config.WEIGHT_SEMANTIC_RETRIVER],
            )
            logger.info(f"configuracion de retriver compuesto establecido")
        except Exception as e:
            logger.error(f'Error inesperado en la configuracion de retriver compuesto establecido, descripcion: {e}') 
            

    def getRetriever(self):
        return self.retriver

    def getKDocuments(documents, k):
        if len(documents) <= k:
            return documents
        return documents[:k]

    def reordenDocumentos(documents):
        reordering = LongContextReorder()
        reordered_docs = reordering.transform_documents(documents)
        return reordered_docs

    def searchDocuments(query):
        return query
