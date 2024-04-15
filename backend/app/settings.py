import os
from typing import Dict
from llama_index.core.settings import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere

def llm_config_from_env() -> Dict:
    from llama_index.core.constants import DEFAULT_TEMPERATURE

    model = os.getenv("MODEL")
    temperature = os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE)
    max_tokens = os.getenv("LLM_MAX_TOKENS")

    config = {
        "model": model,
        "temperature": float(temperature),
        "max_tokens": int(max_tokens) if max_tokens is not None else None,
    }
    return config


def embedding_config_from_env() -> Dict:
    model = os.getenv("EMBEDDING_MODEL")
    dimension = os.getenv("EMBEDDING_DIM")

    config = {
        "model": model,
        "dimension": int(dimension) if dimension is not None else None,
    }
    return config


def init_settings():
    llm_configs = llm_config_from_env()
    embedding_configs = embedding_config_from_env()
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

    Settings.llm = OpenAI(llm_configs= llm_configs)
    #Settings.llm = Ollama(model="llama2:7b", request_timeout=30.0)
    Settings.llm = Cohere(api_key=COHERE_API_KEY, model="command-r-plus")

    #Settings.embed_model = OpenAIEmbedding()
    #Settings.embed_model= HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.embed_model = CohereEmbedding(
        cohere_api_key=COHERE_API_KEY,
        model_name="embed-english-v3.0",
        input_type="search_query",
    )
    
    Settings.chunk_size = int(os.getenv("CHUNK_SIZE", "1024"))
    Settings.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "20"))
