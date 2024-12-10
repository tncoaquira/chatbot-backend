from typing import Union
from fastapi import FastAPI
from src.database.chatbotDB import engine, Base
import logging
from src.application.baseConocimiento.controllers import documentos, preguntas
from src.application.comunicacion.controllers import comunicacion, sincronizacion
from src.application.autentificacion.controllers import autentificacion
from src.bot.handle import BotHandle
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filemode="w"
)

bot = BotHandle()
bot.inicializarBot()
if not bot.initialized():
    bot.initDataMemory()


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(documentos.router)
app.include_router(preguntas.router)
app.include_router(comunicacion.router)
app.include_router(sincronizacion.router)
app.include_router(autentificacion.router)


origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"helloo"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
