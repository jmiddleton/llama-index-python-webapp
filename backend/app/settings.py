import os
from typing import Dict
from llama_index.core.settings import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from llama_index.llms.anthropic import Anthropic
# from llama_index.llms.ollama import Ollama

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

    Settings.llm = OpenAI()
    #Settings.llm = Anthropic(model="claude-3-opus-20240229", temperature=0.0)
    #Settings.llm = Ollama(model="llama2", request_timeout=260.0)
    
    #Settings.embed_model = OpenAIEmbedding()
    Settings.embed_model= HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")
    Settings.chunk_size = int(os.getenv("CHUNK_SIZE", "1024"))
    Settings.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "20"))
