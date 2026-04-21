import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from config import (
    DEFAULT_FETCH_K,
    DEFAULT_K,
    EVAL_PATH,
    EVAL_RESULTS_PATH,
)
from models import get_chat_model
from rag_pipeline import answer_question, load_vector_store


def load_eval_questions(path):
    with open(path, "r") as file:
        return json.load(file)


def source_matches(actual_sources, expected_sources):
    return any(source in actual_sources for source in expected_sources)


def keyword_score(answer, expected_keywords):
    answer_lower = answer.lower()
    matches = [
        keyword
        for keyword in expected_keywords
        if keyword.lower() in answer_lower
    ]

    if not expected_keywords:
        return 0, []

    return len(matches) / len(expected_keywords), matches


def run_question(db, model, question_data, search_type, k, fetch_k):
    question = question_data["question"]

    response = answer_question(
        question,
        db=db,
        model=model,
        search_type=search_type,
        k=k,
        fetch_k=fetch_k,
    )
    results = response["results"]
    answer = response["answer"]

    actual_sources = [
        doc.metadata.get("source")
        for doc, _score in results
    ]

    scores = [
        score
        for _doc, score in results
    ]

    expected_sources = question_data.get("expected_sources", [])
    expected_keywords = question_data.get("expected_keywords", [])

    source_hit = source_matches(actual_sources, expected_sources)
    kw_score, matched_keywords = keyword_score(answer, expected_keywords)

    return {
        "id": question_data["id"],
        "question": question,
        "answer": answer,
        "actual_sources": actual_sources,
        "expected_sources": expected_sources,
        "source_hit": source_hit,
        "similarity_scores": scores,
        "expected_keywords": expected_keywords,
        "matched_keywords": matched_keywords,
        "keyword_score": kw_score,
    }


def resolve_output_path(output_path):
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return Path(EVAL_RESULTS_PATH) / f"eval-results-{timestamp}.json"

    path = Path(output_path)
    if path.parent == Path("."):
        return Path(EVAL_RESULTS_PATH) / path

    return path


def main():
    load_dotenv()

    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=DEFAULT_K)
    parser.add_argument(
        "--search-type",
        choices=["similarity", "mmr"],
        default="similarity",
    )
    parser.add_argument("--fetch-k", type=int, default=DEFAULT_FETCH_K)
    parser.add_argument("--eval-file", type=str, default=EVAL_PATH)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    eval_questions = load_eval_questions(args.eval_file)

    db = load_vector_store()
    model = get_chat_model()

    results = [
        run_question(
            db,
            model,
            question_data,
            args.search_type,
            args.k,
            args.fetch_k,
        )
        for question_data in eval_questions
    ]

    total = len(results)
    source_hits = sum(1 for result in results if result["source_hit"])
    avg_keyword_score = sum(
        result["keyword_score"]
        for result in results
    ) / total

    summary = {
        "total_questions": total,
        "source_hit_rate": source_hits / total,
        "average_keyword_score": avg_keyword_score,
    }

    report = {
        "created_at": datetime.now().isoformat(),
        "k": args.k,
        "search_type": args.search_type,
        "fetch_k": args.fetch_k,
        "summary": summary,
        "results": results,
    }

    output_path = resolve_output_path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as file:
        json.dump(report, file, indent=2)

    print(json.dumps(summary, indent=2))
    print(f"Saved detailed results to {output_path}")


if __name__ == "__main__":
    main()
