from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from backend.api.main import settings

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        self.collection_name = "articles"
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            self.client.get_collection(self.collection_name)
        except:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

    def upsert_article(self, article_id, text, metadata):
        vector = self.model.encode(text).tolist()
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(id=article_id, vector=vector, payload=metadata)
            ]
        )

    def search(self, query, limit=5):
        vector = self.model.encode(query).tolist()
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=limit
        )
