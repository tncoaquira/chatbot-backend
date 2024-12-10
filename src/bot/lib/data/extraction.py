from bs4 import BeautifulSoup, SoupStrainer
from langchain_community.document_loaders import RecursiveUrlLoader
import html2text
from functools import partial
import logging
import time

logger = logging.getLogger(__name__)

def scrapeWeb(
    web_url,
    use_async,
    timeout_seconds,
    max_depth,
    exclude_dirs,
):
    NRO_INTENTOS = 3
    TIEMPO_ESPERA = 10
    loader_pages = partial(
        RecursiveUrlLoader,
        web_url,
        prevent_outside=True,
        check_response_status=True,
        use_async=use_async,
        max_depth=max_depth,
        timeout=60 * timeout_seconds,
        exclude_dirs=exclude_dirs,
    )
    for intento in range(NRO_INTENTOS):
        try:
            loader = loader_pages(extractor=tranformToMarkdown)
            docs = loader.load()
            data = {"totalDocs": len(docs), "docs": docs}
            logger.info(f"Extracion de informacion de la web completa")
            return data
        except TimeoutError as te:
            logger.error(f"Ocurrio un error de TimeoutError, en 10s se intentara nuevamente la extracción de la web: {web_url}")
            time.sleep(TIEMPO_ESPERA)
        except Exception as e:
            logger.error(f"Error en la extraccion de informacion de la web: {e}")
            return None
    logger.warning("Se agotaron los intentos de para extracción de documentos")
    return None


def tranformToMarkdown(
    html,
):  #TODO validar la configuracion de tranformador, en base al contexto. Ademas limpiar comentarios
    soup = BeautifulSoup(html, "lxml", parse_only=SoupStrainer(name="article"))

    SCAPE_TAGS = ["nav", "footer", "aside", "script", "style"]
    for tag in soup.find_all(SCAPE_TAGS):
        tag.decompose()

    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.protect_links = True
    converter.ignore_images = True
    converter.images_to_alt = True
    converter.include_sup_sub = True
    converter.mark_code = True
    converter.body_width = 0
    converter.single_line_break = True
    try:
        text_content = converter.handle(str(soup))
        logger.info(f"Conversion de documentos a markdown completada")
    except Exception as e:
        logger.error(f"Error convertir html a markdown: {e}")
    return text_content
