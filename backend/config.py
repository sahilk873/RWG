from pydantic import BaseSettings


class Config(BaseSettings):
    pinecone_api_key: str
    openai_api_key: str
    input_file_path: str = "revolution.txt"
    entities_output_file: str = "structured_entities_output_new.json"
    relationships_output_file: str = "structured_relationships_output_new.json"
    openai_model: str = "gpt-4o-2024-08-06"
    index_name: str = "relationships-index"
    embedding_dimension: int = 1536

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


_config = Config()


PINECONE_API_KEY = _config.pinecone_api_key
OPENAI_API_KEY = _config.openai_api_key
INPUT_FILE_PATH = _config.input_file_path
ENTITIES_OUTPUT_FILE = _config.entities_output_file
RELATIONSHIPS_OUTPUT_FILE = _config.relationships_output_file
OPENAI_MODEL = _config.openai_model
INDEX_NAME = _config.index_name
EMBEDDING_DIMENSION = _config.embedding_dimension
