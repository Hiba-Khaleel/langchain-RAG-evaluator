from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma

from config import CHROMA_PATH, DEFAULT_FETCH_K, DEFAULT_K, PROMPT_TEMPLATE
from models import get_chat_model, get_embeddings


def load_vector_store():
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embeddings(),
    )


def retrieve_results(db, question, search_type="similarity", k=DEFAULT_K, fetch_k=DEFAULT_FETCH_K):
    if search_type == "similarity":
        return db.similarity_search_with_relevance_scores(question, k=k)

    docs = db.max_marginal_relevance_search(
        question,
        k=k,
        fetch_k=fetch_k,
    )
    return [(doc, None) for doc in docs]


def build_prompt(question, results):
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    return prompt_template.format(context=context_text, question=question)


def answer_question(
    question,
    db=None,
    model=None,
    search_type="similarity",
    k=DEFAULT_K,
    fetch_k=DEFAULT_FETCH_K,
):
    vector_store = db or load_vector_store()
    chat_model = model or get_chat_model()
    results = retrieve_results(vector_store, question, search_type, k, fetch_k)
    prompt = build_prompt(question, results)
    answer = chat_model.invoke(prompt).content

    return {
        "answer": answer,
        "prompt": prompt,
        "results": results,
        "sources": [doc.metadata.get("source") for doc, _score in results],
        "scores": [score for _doc, score in results],
    }
