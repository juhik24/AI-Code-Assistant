import ast
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)


def character_chunk(document):
    """Fallback chunking for non-Python files."""
    chunks = []

    split_text = splitter.split_text(document["content"])

    for i, chunk in enumerate(split_text):
        chunks.append({
            "id": f"{document['path']}_{i}",
            "text": chunk,
            "source": document["path"],
        })

    return chunks


def python_chunk(document):
    """Chunk Python files by top-level classes and functions."""
    code = document["content"]
    source = document["path"]

    try:
        tree = ast.parse(code)
    except SyntaxError:
        # If parsing fails, fall back to character chunking
        return character_chunk(document)

    chunks = []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            chunk = ast.get_source_segment(code, node)

            if chunk:
                chunks.append({
                    "id": f"{source}_{node.name}",
                    "text": chunk,
                    "source": source,
                })

    # If no functions/classes were found, fall back
    if not chunks:
        return character_chunk(document)

    return chunks


def chunk_documents(documents):
    chunks = []

    for document in documents:
        extension = Path(document["path"]).suffix

        if extension == ".py":
            chunks.extend(python_chunk(document))
        else:
            chunks.extend(character_chunk(document))

    return chunks