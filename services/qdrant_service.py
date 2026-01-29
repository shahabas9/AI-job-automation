from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.models import SearchRequest

class QdrantService:
    def __init__(self, collection_name: str, vector_size: int):
        self.client = QdrantClient(url="http://localhost:6333")
        self.collection_name = collection_name
        self.vector_size = vector_size

        self._init_collection()

    def _init_collection(self):
        collections = self.client.get_collections().collections
        if self.collection_name not in [c.name for c in collections]:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )

    def upsert(self, point_id: str, vector: list, payload: dict):
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            ]
        )
    def search(self, query_vector: list, limit: int = 10):
        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit
        )

        # response.points is the list of ScoredPoint
        return response.points

    def clear(self):
        """Delete all points from the collection"""
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            self._init_collection()  # Recreate the collection
        except Exception as e:
            print(f"Error clearing collection: {e}")
