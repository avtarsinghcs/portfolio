import os

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

EMBED_MODEL = "BAAI/bge-small-en-v1.5"

EMBED_DIM = 384

COLLECTION_NAME = "ragbot_collection"

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

TOP_K = 5