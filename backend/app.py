# builtin
from contextlib import asynccontextmanager

# external
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pinecone import Pinecone

# internal
from utils import produce_context
from query import query_database
from openai_methods import (
    user_output_generation,
    create_embedding,
    extract_relationship_type,
)
from config import PINECONE_API_KEY
from models import EntityMetadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index('relationships-index')
    app.state.pc = pc
    app.state.index = index
    yield
    print("Shutting down")
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://revolutionary-war-graph-71wc.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

class QuestionRequest(BaseModel):
    question: str
    num_matches: int = 5

class QuestionResponse(BaseModel):
    answer: str
    context: list[str]

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: Request, question_request: QuestionRequest):
    app = request.app
    user_question: str = question_request.question.strip()
    num_matches: int = question_request.num_matches

    if not user_question:
        raise HTTPException(status_code=400, detail="Please enter a valid question.")

    relationship_type: str = extract_relationship_type(question=user_question)
    relationship_embedding: list[float] = create_embedding(text=relationship_type)

    index = app.state.index
    results = query_database(
        index, k_num=num_matches, relationship_embedding=relationship_embedding, index=index
    )

    entity_dict: dict[int, EntityMetadata] = {}
    for i, match in enumerate(results['matches']):
        entity = EntityMetadata(
            entity1_id=match['metadata'].get('entity1_id'),
            entity2_id=match['metadata'].get('entity2_id'),
            relationship=match['metadata'].get('relationship_type')
        )
        entity_dict[i] = entity

    context: list[str] = produce_context(entity_dict=entity_dict)
    answer: str = user_output_generation(question=user_question, context=context)

    response = QuestionResponse(
        answer=answer,
        context=context
    )
    return response
