import logging


from pprint import pprint

from typing import Sequence
from operator import itemgetter
from langchain.schema import BaseRetriever, Document, StrOutputParser
from langchain.base_language import BaseLanguageModel
from langchain.schema.messages import BaseMessageChunk
from src.bot.templates import contexto
from langchain.schema.runnable import Runnable, RunnableMap
from langchain_community.document_transformers import LongContextReorder
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from functools import partial


logger = logging.getLogger(__name__)


def format_docs(docs: Sequence[Document]) -> str:
    formatted_docs: list[str] = []
    for i, doc in enumerate(docs):
        doc_string = f"<doc id='{i}'>{doc.page_content}</doc>"
        formatted_docs.append(doc_string)
    return "\n".join(formatted_docs)


def get_k_or_less_documents(documents: list[Document], k: int):
    if len(documents) <= k:
        return documents
    else:
        return documents[:k]


def reorder_documents(documents: list[Document]):
    reorder = LongContextReorder()
    return reorder.transform_documents(documents)


def create_retriever_chain(
    llm: BaseLanguageModel[BaseMessageChunk],
    retriever: BaseRetriever,
    use_chat_history: bool,
):
    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(
        contexto.CONDENSE_QUESTION_TEMPLATE
    )
    if not use_chat_history:

        initial_chain = itemgetter("question") | retriever
        return initial_chain
    else:
        condense_question_chain = (
            {
                "question": itemgetter("question"),
                "chat_history": itemgetter("chat_history"),
            }
            | CONDENSE_QUESTION_PROMPT
            | llm
            | StrOutputParser()
        )
        conversation_chain = condense_question_chain | retriever
        def conversation_chain_with_print(input_data):
            result = conversation_chain(input_data)
            print("input_data:", input_data)
            print("Documents retrieved with chat history:", result)
            return result
        return conversation_chain_with_print


def create_answer_chain(
    llm: BaseLanguageModel[BaseMessageChunk],
    retriever: BaseRetriever,
    use_chat_history: bool,
    k: int = 5,
) -> Runnable:
    retriever_chain = create_retriever_chain(llm, retriever, use_chat_history)

    _get_k_or_less_documents = partial(get_k_or_less_documents, k=k)

    context = RunnableMap(
        {
            "context": (
                retriever_chain
                | _get_k_or_less_documents
                | reorder_documents
                | format_docs
            ),
            "question": itemgetter("question"),
        }
    )

    prompt = ChatPromptTemplate.from_messages(
        messages=[
            ("system", contexto.SYSTEM_ANSWER_QUESTION_TEMPLATE),
            ("human", "{question}"),
        ]
    )
    response_synthesizer = prompt | llm | StrOutputParser()
    response_chain = context | response_synthesizer
    

    return response_chain
