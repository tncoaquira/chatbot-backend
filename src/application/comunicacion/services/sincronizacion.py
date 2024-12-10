from src.bot.handle import BotHandle
from src.bot.lib.memory import ingesta
from src.application.baseConocimiento.services import conocimiento
import logging
from src.common.utils import responseFormatter

logger = logging.getLogger(__name__)


def sincronizarDatabaseService():
    try:
        bot = BotHandle()
        bot.sincronizarBaseRelacional()
    except Exception as e:
        logger.error(e)
        responseFormatter.errorResponse(
            detail=e, message="DB: Ocurrio al sincronizar la base de conocimiento", status_code=500
        )
    return {}
