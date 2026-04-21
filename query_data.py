import argparse
import os
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from config import (
    CHROMA_PATH,
    DEFAULT_K,
    DEFAULT_RELEVANCE_THRESHOLD,
    PROMPT_TEMPLATE,
)
from models import get_chat_model, get_embeddings

load_dotenv()


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    if not os.path.exists(CHROMA_PATH):
        raise ValueError("Chroma database is missing. Run `python3 create_db.py` first.")

    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    parser.add_argument("--k", type=int, default=DEFAULT_K)
    parser.add_argument("--threshold", type=float, default=DEFAULT_RELEVANCE_THRESHOLD)
    parser.add_argument("--debug", action="store_true", help="Print the generated prompt.")
    args = parser.parse_args()
    query_text = args.query_text

    # Prepare the DB.
    embedding_function = get_embeddings()
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function,
    )

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=args.k)
    if len(results) == 0 or results[0][1] < args.threshold:
        print("Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    if args.debug:
        print(prompt)

    model = get_chat_model()
    response_text = model.invoke(prompt).content

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()
