#external
from pinecone import Pinecone, ServerlessSpec

def query_database(index, k_num:int,  relationship_embedding: list[float]) -> dict[str, any]:
    assert isinstance(k_num, int)
    assert isinstance(relationship_embedding, list)
    results = index.query(
        vector=relationship_embedding,
        top_k=k_num,
        include_values=False,
        include_metadata=True)
    return results

