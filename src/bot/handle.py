import logging

from .lib.memory import ingesta
from .lib.memory.embedding import EmbedderHuggingFace
from .lib.memory.vertorStore import VectorMemory
from src.config import database, chatbot
from .lib.data import extraction, splitters
from .lib.memory import ingesta
from pprint import pprint
from langchain_community.retrievers import BM25Retriever
from .lib.memory.retriver import RetriverModel
from langchain_community.llms import Ollama
from .constante.index import MODELO_EMBEDDING, URLS_IGNORE
from src.application.baseConocimiento.services import conocimiento
from src.common.baseSingleton import SingletonBase
from .lib.conversacion import chains
from langchain_openai import ChatOpenAI
import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI

logger = logging.getLogger(__name__)


class BotHandle(SingletonBase):
    def __init__(self):
        self.vector_store: VectorMemory = None
        self.re_chain = None
        self.answer_chain = None

    def getOrBuildMemory(self):
        model_name = MODELO_EMBEDDING
        chroma_collection = chatbot.Config.VECTOR_STORE_DIR
        chroma_persist_dir = chatbot.Config.VECTOR_STORE_PERSIST_DIR
        sqlRecord_db_url = database.Config.PG_RECORD_MANAGER

        embedding = EmbedderHuggingFace(model_name).get_embedding()

        self.vector_store = VectorMemory(
            chroma_collection_name=chroma_collection,
            chroma_persist_dir=chroma_persist_dir,
            sqlRecord_db_url=sqlRecord_db_url,
            embedding=embedding,
        )

    def sincronizarBaseRelacional(self):
        documentosDB = conocimiento.getDocumentosEstructuradosService()
        print("documentosDB", documentosDB)
        ingesta.ingestaPorDocumentos(
            vector_store=self.vector_store, clean_vector=False, documentos=documentosDB
        )

    def initDataMemory(self):
        ingesta.ingestaPorWeb(
            vector_store=self.vector_store,
            clean_vector=True,
            web_url=chatbot.Config.BASE_URL_EXTRACTION,
            use_async=False,
            timeout_seconds=5,
            max_depth=3,
            exclude_dirs=URLS_IGNORE,
        )

    def initialized(self):
        vector_store = self.vector_store
        if vector_store.existsDocuments():
            return True
        return False

    def updateDataMemory(self):
        data = extraction.scrapeWeb(
            web_url="https://ubp.com.bo/",
            use_async=False,
            timeout_seconds=3,
            max_depth=5,
            exclude_dirs=(),
        )
        data_split = splitters.splitDocumentos(data["docs"])
        vector_store = self.vector_store
        vector_store.clear()
        vector_store.clearDataIncremental(data_split["docs"])

    def inicializarBot(self):
        self.getOrBuildMemory()

        vector_store = self.vector_store.getVectorStore()
        docs = self.vector_store.getDocuments()
        keyword_r = BM25Retriever.from_documents(docs)
        keyword_r.k = 0
        semantic_r = vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": 4}
        )
        retriever = RetriverModel(
            keyword_retriver=keyword_r, semantic_retriver=semantic_r
        ).getRetriever()

        if not os.environ.get("GOOGLE_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = getpass.getpass(
                "Enter your google API key: "
            )
        try:
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")

        answer_chain = chains.create_answer_chain(
            llm=llm, retriever=retriever, use_chat_history=False, k=6
            
        )
        self.answer_chain = answer_chain


if __name__ == "__main__":
    bot = BotHandle()
    bot.inicializarBot()
