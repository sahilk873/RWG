# builtin
import os  

# external
from pinecone import * 

#internal  
from query import query_database
from openai_methods import user_output_generation, create_embedding, extract_relationship_type
from utils import produce_context
from config import PINECONE_API_KEY 
from models import EntityMetadata

pc: Pinecone = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index('relationships-index')

def main() -> None:
    print("=== Revolutionary War Relationship Type Generator ===\n")
    print("Enter your questions related to the Revolutionary War. Type 'exit' to quit.\n")

    while True:
        user_question: str = input("Your Question: ").strip()

        if user_question.lower() in ['exit', 'quit']:
            print("Exiting the Revolutionary War Chatbot!")
            break

        if not user_question:
            print("Please enter a valid question.\n")
            continue

        relationship_type: str = extract_relationship_type(user_question) # name ur args

        relationship_embedding: list[float] = create_embedding(relationship_type)

        results: dict[str, any] = query_database(index, 3, relationship_embedding)

        entity_dict: dict[int, EntityMetadata] = {}

        for i, match in enumerate(results['matches']):
            entity = EntityMetadata(entity1_id=match['metadata'].get('entity1_id'), 
                                    entity2_id=match['metadata'].get('entity2_id'), 
                                    relationship=match['metadata'].get('relationship_type'))
            entity_dict[i] = entity

        context: list[str] = produce_context(entity_dict)
        
        answer: str = user_output_generation(user_question, context)

        print(answer)


if __name__ == "__main__":
    main()

