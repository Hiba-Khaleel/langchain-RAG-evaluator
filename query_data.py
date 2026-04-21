import argparse
import os
from dotenv import load_dotenv

from config import (
    CHROMA_PATH,
    DEFAULT_K,
    DEFAULT_RELEVANCE_THRESHOLD,
)
from rag_pipeline import answer_question

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

    response = answer_question(query_text, k=args.k)
    results = response["results"]
    if len(results) == 0 or results[0][1] < args.threshold:
        print("Unable to find matching results.")
        return

    if args.debug:
        print(response["prompt"])

    formatted_response = f"Response: {response['answer']}\nSources: {response['sources']}"
    print(formatted_response)


if __name__ == "__main__":
    main()
