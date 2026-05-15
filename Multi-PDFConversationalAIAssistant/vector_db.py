from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from config import (
    EMBED_DIM,
    COLLECTION_NAME
)


class QdrantStorage:

    def __init__(self):

        self.client = QdrantClient(
            ":memory:"
        )

        try:

            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=EMBED_DIM,
                    distance=Distance.COSINE
                )
            )

        except:
            pass

    def upsert(
        self,
        ids,
        vectors,
        payloads
    ):

        points = []

        for i in range(len(ids)):

            points.append(
                PointStruct(
                    id=i,
                    vector=vectors[i],
                    payload=payloads[i]
                )
            )

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

    def search(
        self,
        query_vector,
        limit=5
    ):

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit
        ).points

        contexts = []

        sources = []

        for r in results:

            contexts.append(
                r.payload["text"]
            )

            sources.append(
                r.payload["source"]
            )

        return {
            "contexts": contexts,
            "sources": sources
        }