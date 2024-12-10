from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from src.bot.constante.index import MODELO_EMBEDDING, NORMALIZAR_EMBEDDING
from transformers import AutoModel, AutoTokenizer


class EmbedderHuggingFace:
    
    def __init__(
        self, model_name=MODELO_EMBEDDING
    ):

        self.embedder = HuggingFaceEmbeddings(
            model_name=model_name,
            multi_process=True,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": NORMALIZAR_EMBEDDING},
        )

    def get_embedding(self):
        return self.embedder
