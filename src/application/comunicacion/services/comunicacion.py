from src.bot.handle import BotHandle
from ..schemas.index import PreguntaBot


def resolverPreguntaService(preguntaBot: PreguntaBot):
    bot = BotHandle()
    repuesta = bot.answer_chain.invoke(
        {
            "question": preguntaBot.textoPregunta,
            "chat_history": [],
        }
    )
    print('_________________________________________________________________________________')
    print(repuesta)
    return repuesta
