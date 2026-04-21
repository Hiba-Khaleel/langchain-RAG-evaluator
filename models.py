from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config import CHAT_MODEL, CHAT_TEMPERATURE, EMBEDDING_MODEL


def get_embeddings():
    if EMBEDDING_MODEL:
        return OpenAIEmbeddings(model=EMBEDDING_MODEL)

    return OpenAIEmbeddings()


def get_chat_model():
    kwargs = {"temperature": CHAT_TEMPERATURE}

    if CHAT_MODEL:
        kwargs["model"] = CHAT_MODEL

    return ChatOpenAI(**kwargs)
