from pydantic import BaseModel
from typing import List


class RAGChunkAndSource(BaseModel):
    chunks: List[str]
    source_id: str


class RAGUpsertResult(BaseModel):
    ingested: int


class RAGSearchResult(BaseModel):
    contexts: List[str]
    sources: List[str]


class RAGQueryResponse(BaseModel):
    answer: str
    sources: List[str]