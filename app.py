import json
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from config import (
    CHROMA_PATH,
    DEFAULT_FETCH_K,
    DEFAULT_K,
    DEFAULT_RELEVANCE_THRESHOLD,
    EVAL_RESULTS_PATH,
)
from models import get_chat_model
from rag_pipeline import answer_question, load_vector_store

load_dotenv()


st.set_page_config(
    page_title="RAG Evaluator",
    layout="wide",
)


@st.cache_resource
def cached_vector_store():
    return load_vector_store()


@st.cache_resource
def cached_chat_model():
    return get_chat_model()


def load_eval_reports():
    results_dir = Path(EVAL_RESULTS_PATH)
    if not results_dir.exists():
        return []

    reports = []
    for path in sorted(results_dir.glob("*.json")):
        try:
            with open(path, "r") as file:
                report = json.load(file)
        except json.JSONDecodeError:
            continue

        summary = report.get("summary", {})
        reports.append(
            {
                "file": path.name,
                "path": str(path),
                "created_at": report.get("created_at", ""),
                "questions": summary.get("total_questions"),
                "source_hit_rate": summary.get("source_hit_rate"),
                "average_keyword_score": summary.get("average_keyword_score"),
                "report": report,
            }
        )

    return reports


def format_score(score):
    if score is None:
        return "n/a"

    return f"{score:.4f}"


def render_sidebar():
    st.sidebar.header("Retrieval")
    k = st.sidebar.number_input("Top K", min_value=1, max_value=10, value=DEFAULT_K)
    threshold = st.sidebar.slider(
        "Minimum relevance",
        min_value=0.0,
        max_value=1.0,
        value=DEFAULT_RELEVANCE_THRESHOLD,
        step=0.05,
    )
    search_type = st.sidebar.selectbox("Search type", ["similarity", "mmr"])
    fetch_k = st.sidebar.number_input(
        "MMR fetch K",
        min_value=int(k),
        max_value=50,
        value=max(DEFAULT_FETCH_K, int(k)),
    )

    return {
        "k": int(k),
        "threshold": threshold,
        "search_type": search_type,
        "fetch_k": int(fetch_k),
    }


def render_chat(settings):
    st.subheader("Chat With Your Documents")

    if not os.environ.get("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY is missing. Add it to your .env file.")
        return

    if not Path(CHROMA_PATH).exists():
        st.error("Chroma database is missing. Run `python create_db.py` first.")
        return

    db = cached_vector_store()
    model = cached_chat_model()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question about the indexed documents")
    if not question:
        return

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving context and generating an answer..."):
            response = answer_question(
                question,
                db=db,
                model=model,
                search_type=settings["search_type"],
                k=settings["k"],
                fetch_k=settings["fetch_k"],
            )

        first_score = response["scores"][0] if response["scores"] else None
        if (
            settings["search_type"] == "similarity"
            and first_score is not None
            and first_score < settings["threshold"]
        ):
            answer = "Unable to find matching results."
            st.warning(answer)
        else:
            answer = response["answer"]
            st.markdown(answer)

            with st.expander("Sources"):
                for index, (source, score) in enumerate(
                    zip(response["sources"], response["scores"]),
                    start=1,
                ):
                    st.write(f"{index}. `{source}` - score: `{format_score(score)}`")

    st.session_state.messages.append({"role": "assistant", "content": answer})


def render_evaluations():
    st.subheader("Evaluation Results")

    reports = load_eval_reports()
    if not reports:
        st.info("No evaluation reports found. Run `python evaluate.py --output eval-current.json`.")
        return

    rows = [
        {
            "file": report["file"],
            "created_at": report["created_at"],
            "questions": report["questions"],
            "source_hit_rate": report["source_hit_rate"],
            "average_keyword_score": report["average_keyword_score"],
        }
        for report in reports
    ]

    st.dataframe(rows, use_container_width=True)

    best = max(
        reports,
        key=lambda report: report["average_keyword_score"] or 0,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Best report", best["file"])
    col2.metric("Source hit rate", format_score(best["source_hit_rate"]))
    col3.metric("Keyword score", format_score(best["average_keyword_score"]))

    selected_file = st.selectbox(
        "Inspect report",
        [report["file"] for report in reports],
        index=[report["file"] for report in reports].index(best["file"]),
    )
    selected = next(report for report in reports if report["file"] == selected_file)
    report = selected["report"]

    st.markdown("#### Per-Question Results")
    details = []
    for result in report.get("results", []):
        details.append(
            {
                "id": result.get("id"),
                "source_hit": result.get("source_hit"),
                "keyword_score": result.get("keyword_score"),
                "matched_keywords": ", ".join(result.get("matched_keywords", [])),
                "actual_sources": ", ".join(
                    source for source in result.get("actual_sources", []) if source
                ),
            }
        )

    st.dataframe(details, use_container_width=True)

    with st.expander("Raw JSON"):
        st.json(report)


def main():
    st.title("RAG Evaluator")
    st.caption("Chat with indexed documents and inspect saved evaluation runs.")

    settings = render_sidebar()
    chat_tab, eval_tab = st.tabs(["Chat", "Evaluations"])

    with chat_tab:
        render_chat(settings)

    with eval_tab:
        render_evaluations()


if __name__ == "__main__":
    main()
