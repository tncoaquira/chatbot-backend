from ..data.extraction import scrapeWeb
from ..data.splitters import splitDocumentos


def ingestaPorWeb(
    vector_store,
    clean_vector,
    web_url,
    use_async,
    timeout_seconds,
    max_depth,
    exclude_dirs,
):
    data = scrapeWeb(
        web_url=web_url,
        use_async=use_async,
        timeout_seconds=timeout_seconds,
        max_depth=max_depth,
        exclude_dirs=exclude_dirs,
    )

    data_split = splitDocumentos(data["docs"])

    if clean_vector:
        vector_store.clear()
        vector_store.clearDataFull(data_split["docs"])
    else:
        vector_store.clearDataIncremental(data_split["docs"])


def ingestaPorDocumentos(vector_store, clean_vector, documentos):
    if clean_vector:
        vector_store.clear()
        vector_store.clearDataFull(documentos)
    else:
        vector_store.clearDataIncremental(documentos)
