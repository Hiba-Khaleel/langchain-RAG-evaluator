from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import shutil

from config import CHROMA_PATH, CHUNK_OVERLAP, CHUNK_SIZE, DATA_PATH
from models import get_embeddings

load_dotenv()


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md", loader_cls=TextLoader)
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    if chunks:
        document = chunks[min(10, len(chunks) - 1)]
        print(document.page_content)
        print(document.metadata)

    return chunks


# Create new database from the documents.
def save_to_chroma(chunks: list[Document]):
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(
        chunks,
        get_embeddings(),
        persist_directory=CHROMA_PATH,
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)
