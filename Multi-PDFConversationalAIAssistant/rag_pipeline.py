import uuid

from data_loader import (
    load_and_chunk_pdf,
    embed_texts
)

from vector_db import QdrantStorage

from llm import generate_answer

from config import TOP_K


db = QdrantStorage()


def ingest_pdf(
    pdf_path: str,
    source_id: str
):

    chunks = load_and_chunk_pdf(
        pdf_path
    )

    embeddings = embed_texts(
        chunks
    )

    ids = []

    payloads = []

    for i in range(len(chunks)):

        ids.append(
            str(uuid.uuid4())
        )

        payloads.append(
            {
                "text": chunks[i],
                "source": source_id,
                "chunk_id": i
            }
        )

    db.upsert(
        ids=ids,
        vectors=embeddings,
        payloads=payloads
    )

    return {
        "status": "success",
        "chunks_ingested": len(chunks),
        "document": source_id
    }


def query_rag(
    question: str
):

    query_embedding = embed_texts(
        [question]
    )[0]

    search_results = db.search(
        query_vector=query_embedding,
        limit=TOP_K
    )

    grouped_context = {}

    for i in range(
        len(search_results["contexts"])
    ):

        source = search_results["sources"][i]

        context = search_results["contexts"][i]

        if source not in grouped_context:

            grouped_context[source] = []

        grouped_context[source].append(
            context
        )

    formatted_context = ""

    for source, contexts in grouped_context.items():

        formatted_context += f"\n\n===== DOCUMENT: {source} =====\n\n"

        for c in contexts:

            formatted_context += c + "\n\n"

    answer = generate_answer(
        question=question,
        contexts=[formatted_context]
    )

    return {
        "answer": answer,
        "sources": search_results["sources"],
        "contexts_found": len(
            search_results["contexts"]
        ),
        "documents_used": list(
            grouped_context.keys()
        )
    }