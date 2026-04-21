# RAG LangChain App: Progress Notes

## Project Goal

This project is a small Retrieval-Augmented Generation app for asking questions about the Eiffel programming language guide.

The app uses local Markdown files as the knowledge source, stores document embeddings in Chroma, retrieves relevant chunks for a user question, and sends the retrieved context to an OpenAI chat model to generate an answer.

## Current Architecture

The project currently has two main scripts:

- `create_db.py`
  - Loads Markdown files from `data/eiffel-guide`.
  - Splits the documents into smaller chunks.
  - Creates embeddings using `OpenAIEmbeddings`.
  - Stores the chunks and embeddings in a local Chroma database.

- `query_data.py`
  - Accepts a user question from the command line.
  - Loads the existing Chroma database.
  - Retrieves the top 3 most relevant chunks.
  - Builds a prompt using the retrieved context.
  - Sends the prompt to `ChatOpenAI`.
  - Prints the generated answer and source files.

## Baseline Retrieval Setup

The current retrieval setup uses:

- Chroma as the vector database.
- OpenAI embeddings.
- Similarity search.
- `k=3`, meaning the retriever returns the top 3 matching chunks.
- A simple prompt that instructs the model to answer based only on the retrieved context.

The current chunking setup in `create_db.py` uses:

- `chunk_size=300`
- `chunk_overlap=100`

This is a small chunk size with relatively high overlap. It works for a starter project, but it may create fragmented chunks and duplicate retrieval results.

## Evaluation Added

We added an evaluation process so future optimizations can be measured instead of guessed.

The evaluation uses:

- `evals/eval_questions.json`
  - Contains test questions.
  - Defines the expected source file for each question.
  - Defines expected keywords that should appear in the answer.

- `evaluate.py`
  - Runs each evaluation question through the current RAG pipeline.
  - Records retrieved source files.
  - Records similarity scores.
  - Generates an answer using the chat model.
  - Checks whether the expected source was retrieved.
  - Checks how many expected keywords appeared in the answer.
  - Saves detailed results to a JSON report.

## Baseline Result

The baseline evaluation was run with:

```bash
python evaluate.py --k 3 --output eval-baseline.json
```

The summary result was:

```json
{
  "total_questions": 5,
  "source_hit_rate": 1.0,
  "average_keyword_score": 0.4333333333333333
}
```

The detailed baseline measurement record is saved in `BASELINE_MEASUREMENTS.md`.

The first retrieval optimization experiment is saved in `MMR_MEASUREMENTS.md`.

The larger chunking experiment is saved in `CHUNK_800_MEASUREMENTS.md`.

The expanded evaluation result is saved in `EXPANDED_EVAL_MEASUREMENTS.md`.

## Optimization Results So Far

| Experiment | Source Hit Rate | Average Keyword Score | Result |
| --- | ---: | ---: | --- |
| Baseline similarity search, chunk size 300 | 1.0 | 0.4333 | Working baseline |
| MMR retrieval, chunk size 300 | 1.0 | 0.4333 | More diverse retrieval, no score improvement |
| Similarity search, chunk size 800 | 1.0 | 0.7333 | Best result so far |
| Prompt v2 with expanded evaluation set | 1.0 | 0.8889 | Current best measurement |

The strongest improvement came from increasing chunk size from `300` to `800` and using `120` overlap. This suggests that the model needed larger context windows to produce more complete technical answers.

After improving the prompt and expanding the evaluation set to 6 questions, the system reached an average keyword score of `0.8889` while keeping source hit rate at `1.0`.

## What The Baseline Means

`total_questions: 5` means the evaluation used 5 test questions.

`source_hit_rate: 1.0` means the correct source file appeared in the retrieved top 3 chunks for every question. This is a good sign: the retrieval layer is finding the right documents.

`average_keyword_score: 0.4333` means the generated answers included about 43% of the expected keywords on average. This is weaker, but it does not automatically mean the answers are wrong. Some answers used related words instead of the exact expected keywords.

For example, an answer about contracts may say "preconditions" and "postconditions", while the expected keywords are `require` and `ensure`. The answer can be conceptually related but still receive a lower keyword score.

## Key Observations

The baseline shows that retrieval is generally finding the right files.

Some retrieved results include repeated chunks from the same source file. For example, the loops question retrieved three chunks from `18-loops.md`. This can be useful when the whole answer is in one document, but it can also waste context space.

The MMR experiment increased retrieval diversity but did not improve the current keyword score.

The larger chunking experiment improved the average keyword score from `0.4333` to `0.7333` while keeping source hit rate at `1.0`.

Prompt v1 reduced the score because it made answers too concise and caused the model to drop important technical terms. Prompt v2 recovered the score by explicitly asking for Eiffel-specific terminology.

The expanded evaluation set improved the agents test by aligning expected keywords with the actual source document and adding a targeted question about passing arguments through agents.

The answer quality metric is currently simple. Keyword matching is useful for a first baseline because it is repeatable and easy to understand, but it is not a complete measure of correctness.

## Current Strengths

- The basic RAG pipeline works end to end.
- The app can answer questions using local documentation.
- Source files are returned with answers.
- Evaluation now gives a measurable baseline.
- The baseline retrieval source hit rate is strong.

## Current Limitations

- Chunking is character-based and not Markdown-aware.
- Chunk size may be too small for full explanations.
- Retrieval uses basic similarity search, which can return duplicate or very similar chunks.
- The prompt is simple and may not encourage complete technical answers.
- Evaluation uses exact keyword matching, which misses semantically correct wording.
- Model and embedding defaults are not explicitly configured.

## Optimization Direction

The next optimization steps should be measured against `evals/results/eval-baseline.json`.

Recommended order:

1. Keep the larger chunking configuration for now.
2. Make model settings explicit, especially `temperature=0`.
3. Improve the prompt so the answer includes relevant technical terms and admits when context is insufficient.
4. Add more evaluation questions before making more optimization decisions.
5. Consider Markdown-aware splitting after the evaluation set is larger.
6. Improve evaluation with manual review labels or LLM-based judging.

## Presentation Story So Far

The project started as a simple RAG app over Eiffel guide Markdown files.

Before optimizing, we added evaluation so changes can be compared against a baseline.

The first baseline shows that the retriever is finding the right documents, but the generated answers do not always include the expected technical details.

The first optimization, MMR retrieval, preserved retrieval accuracy and increased diversity, but did not improve the measured keyword score.

The second optimization, larger chunks, produced the strongest result so far: source hit rate stayed at `1.0`, and average keyword score improved from `0.4333` to `0.7333`.

The next optimization, prompt v2 plus an expanded evaluation set, reached `0.8889` average keyword score across 6 questions while keeping source hit rate at `1.0`.

This gives us a clear optimization target: preserve the strong source hit rate and the improved answer completeness while validating the result against a larger evaluation set.
