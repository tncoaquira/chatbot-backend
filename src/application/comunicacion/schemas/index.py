from pydantic import BaseModel


class PreguntaBot(BaseModel):
    textoPregunta: str
