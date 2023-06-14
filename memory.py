import chromadb
from chromadb.config import Settings


class Memory:

    """Memory for the agent and evaluator."""

    def __init__(self):
        self._client = chromadb.Client(
            Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory="persistence_of_memory",
            )
        )

        # Get the existing collections and store them as a dict
        self._collections = {
            collection.name: collection
            for collection in self._client.list_collections()
        }

    def create_collection(self, name: str):
        if name not in self._collections:
            self._collections[name] = self._client.get_or_create_collection(name)

    def upsert(self, collection_name: str, data: dict):
        self._collections[collection_name].upsert(**data)
