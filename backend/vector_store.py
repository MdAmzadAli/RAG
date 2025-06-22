from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from dotenv import load_dotenv
import os
load_dotenv()
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
COLLECTION_NAME="document_rag"

def upsert_to_qdrant(vectors, chunks, user_id, file_id):
    points=[
        PointStruct(
            id=f"{file_id}_{user_id}_{i}",
            vector=vec,
            payload={"text":chunk, "file_id":file_id, "user_id":user_id}
        )
        for i, (vec,chunk) in enumerate(zip(vectors,chunks))
    ]
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

def query_qdrant(query_vec, user_id, file_id, top_k=5):
    result=client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vec,
        limit=top_k,
        filter={
            "must":[
                {"key":"user_id","match":{"value":user_id}},
                {"key":"file_id","match":{"value":file_id}}
            ]
        }
    )
    return [r.payload["text"] for r in result]


def delete_file_from_qdrant(user_id: str, file_id: str):
    filter_condition = {
        "must": [
            {"key": "user_id", "match": {"value": user_id}},
            {"key": "file_id", "match": {"value": file_id}}
        ]
    }
    client.delete(collection_name=COLLECTION_NAME, filter=filter_condition)
    print(f"Deleted vectors for file_id={file_id} and user_id={user_id}")