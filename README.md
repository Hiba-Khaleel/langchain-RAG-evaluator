# LangChain RAG Evaluator

A small Retrieval-Augmented Generation pipeline for asking questions over local Markdown documentation and measuring whether changes improve retrieval and answer quality.

The project currently uses the Eiffel guide as sample data, but the code is organized so another Markdown documentation set can be used by changing `DATA_PATH`.

## What It Does

- Loads Markdown files from `data/eiffel-guide`.
- Splits documents into chunks.
- Stores embeddings in a local Chroma database.
- Retrieves relevant chunks for a user question.
- Sends the retrieved context to an OpenAI chat model.
- Evaluates the RAG pipeline with repeatable test questions.
- Saves evaluation reports for comparison.

## Project Structure

```text
.
├── config.py                  # Shared paths, chunking, retrieval, and prompt settings
├── models.py                  # Shared OpenAI model constructors
├── create_db.py               # Builds the Chroma vector database
├── query_data.py              # CLI for asking questions
├── evaluate.py                # Runs evaluation questions and writes reports
├── app.py                     # Streamlit app for chat and evaluation review
├── data/                      # Source documents
├── chroma/                    # Generated Chroma database, ignored by git
├── evals/
│   ├── eval_questions.json    # Evaluation question set
│   └── results/               # Saved evaluation reports
├── docs/                      # Measurement notes and presentation notes
├── requirements.txt
└── README.md
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create a `.env` file:

```bash
OPENAI_API_KEY=your_api_key_here
```

## Build The Vector Database

Run:

```bash
python create_db.py
```

This loads the Markdown files, splits them, embeds them, and writes the Chroma database to `chroma/`.

The current optimized chunking settings are:

```text
CHUNK_SIZE=800
CHUNK_OVERLAP=120
```

These defaults live in `config.py` and can be overridden with environment variables.

## Ask A Question

Run:

```bash
python query_data.py "What are agents in Eiffel?"
```

Optional flags:

```bash
python query_data.py "How do loops work?" --k 4 --threshold 0.65
```

Use `--debug` to print the full generated prompt:

```bash
python query_data.py "What are contracts in Eiffel?" --debug
```

## Run The Streamlit App

Start the app:

```bash
streamlit run app.py
```

The app has two tabs:

- `Chat`: ask live questions against the Chroma-backed RAG pipeline.
- `Evaluations`: inspect saved reports from `evals/results/`.

The sidebar controls:

- top-k retrieval count
- relevance threshold
- similarity vs MMR retrieval
- MMR fetch count

## Run Evaluation

Run the current evaluation set:

```bash
python evaluate.py --k 3 --output eval-expanded-questions.json
```

Because the output filename has no directory, it will be saved under:

```text
evals/results/eval-expanded-questions.json
```

Run MMR retrieval for comparison:

```bash
python evaluate.py --search-type mmr --k 3 --fetch-k 15 --output eval-mmr-new.json
```

Use a different eval file:

```bash
python evaluate.py --eval-file evals/eval_questions.json --output eval-current.json
```

## Current Best Measurement

The current best measurement is saved in:

```text
evals/results/eval-expanded-questions.json
```

Summary:

```json
{
  "total_questions": 6,
  "source_hit_rate": 1.0,
  "average_keyword_score": 0.8888888888888888
}
```

Current best configuration:

```text
chunk_size=800
chunk_overlap=120
temperature=0
search_type=similarity
k=3
prompt=prompt_v2
```

## Evaluation Metrics

`source_hit_rate` measures whether the expected source document appeared in the retrieved top-k chunks.

`average_keyword_score` measures how many expected keywords appeared in the generated answer.

The keyword score is useful for fast regression checks, but it is not a complete correctness metric. A good answer can still miss an exact expected keyword, and a keyword match does not prove the answer is fully correct.

## Configuration

These environment variables can override defaults:

```bash
DATA_PATH=data/eiffel-guide
CHROMA_PATH=chroma
EVAL_PATH=evals/eval_questions.json
EVAL_RESULTS_PATH=evals/results
CHUNK_SIZE=800
CHUNK_OVERLAP=120
RETRIEVAL_K=3
RETRIEVAL_FETCH_K=15
RELEVANCE_THRESHOLD=0.7
CHAT_TEMPERATURE=0
OPENAI_CHAT_MODEL=
OPENAI_EMBEDDING_MODEL=
```

If `OPENAI_CHAT_MODEL` or `OPENAI_EMBEDDING_MODEL` are empty, LangChain/OpenAI defaults are used.

## Measurement Notes

Detailed optimization notes are in `docs/`:

- `docs/BASELINE_MEASUREMENTS.md`
- `docs/MMR_MEASUREMENTS.md`
- `docs/CHUNK_800_MEASUREMENTS.md`
- `docs/EXPANDED_EVAL_MEASUREMENTS.md`
- `docs/PRESENTATION_NOTES.md`

## Known Notes

Chroma may print telemetry warnings such as:

```text
Failed to send telemetry event ...
```

These warnings do not mean the evaluation failed. If the summary is printed and the JSON report is written, the run completed.

## Next Improvements

- Add more evaluation questions before making more optimization decisions.
- Add manual pass/fail review for answer correctness.
- Consider Markdown-aware chunking once the eval set is larger.
- Consider LLM-as-judge evaluation for groundedness and correctness.
