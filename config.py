import os

DATA_PATH = os.getenv("DATA_PATH", "data/eiffel-guide")
CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma")
EVAL_PATH = os.getenv("EVAL_PATH", "evals/eval_questions.json")
EVAL_RESULTS_PATH = os.getenv("EVAL_RESULTS_PATH", "evals/results")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))

DEFAULT_K = int(os.getenv("RETRIEVAL_K", "3"))
DEFAULT_FETCH_K = int(os.getenv("RETRIEVAL_FETCH_K", "15"))
DEFAULT_RELEVANCE_THRESHOLD = float(os.getenv("RELEVANCE_THRESHOLD", "0.7"))

CHAT_TEMPERATURE = float(os.getenv("CHAT_TEMPERATURE", "0"))
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")

PROMPT_TEMPLATE = """
Answer the question using only the context below.

Rules:
- If the answer is not available in the context, say: "The answer is not available in the provided context."
- Prefer domain-specific terminology from the context over generic wording.
- Include relevant keywords, syntax words, routine names, or type names when they help answer the question.
- Explain the answer in 3-5 sentences.
- Do not use outside knowledge.

Context:
{context}

Question:
{question}

Answer:
"""
