#builtin
from typing import Optional

#external
from openai import OpenAI

#internal
from config import OPENAI_API_KEY

OPENAI_MODEL = "gpt-4o-mini"
client = OpenAI(api_key=OPENAI_API_KEY)

def user_output_generation(question: str, context: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specializing in historical relationships."},
            {"role": "user", "content": f"context: {context}"},
            {"role": "system", "content": question}
        ],
        max_tokens=150,  
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

def create_embedding(text: str) -> list[float]:
    assert isinstance(text, str), "Input must be a string."
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def extract_relationship_type(question: str) -> Optional[str]:
    assert isinstance(question, str), "Input must be a string."
    prompt = f"""
            Given the user's question about the Revolutionary War, identify the relationship type 
            that a hypothetical answer would provide. The relationship type should be a concise phrase 
            that connects two entities involved in the question.

            Question: {question}
            Relationship Type:
            """


    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that identifies relationship types from user questions."
                    "Extract only the relationship type phrase that would appear in a hypothetical answer such as **was was by** or **was found in**."
                    "Return only a string with alphabetical characters"
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=10,  
        temperature=0,   # Deterministic output
        n=1,
    )

    
    relationship_type = response.choices[0].message.content.strip()
    return relationship_type
