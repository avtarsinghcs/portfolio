from llama_index.readers.file import PDFReader

from llama_index.core.node_parser import (
    SentenceSplitter
)

from sentence_transformers import (
    SentenceTransformer
)

from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBED_MODEL
)


embedding_model = SentenceTransformer(
    EMBED_MODEL
)

splitter = SentenceSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)


def load_and_chunk_pdf(
    path: str
):

    docs = PDFReader().load_data(
        file=path
    )

    texts = [
        d.text
        for d in docs
        if getattr(d, "text", None)
    ]

    chunks = []

    for text in texts:

        chunks.extend(
            splitter.split_text(text)
        )

    return chunks


def embed_texts(
    texts: list[str]
):

    embeddings = embedding_model.encode(
        texts
    )

    return embeddings.tolist()