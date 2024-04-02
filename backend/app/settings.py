import os
from typing import Dict
from llama_index.core.settings import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
# from llama_index.llms.anthropic import Anthropic
#from llama_index.llms.huggingface import HuggingFaceLLM
# setup prompts - specific to StableLM
#from llama_index.core import PromptTemplate

# system_prompt = """<|SYSTEM|># StableLM Tuned (Alpha version)
# - StableLM is a helpful and harmless open-source AI language model developed by StabilityAI.
# - StableLM is excited to be able to help the user, but will refuse to do anything that could be considered harmful to the user.
# - StableLM is more than just an information source, StableLM is also able to write poetry, short stories, and make jokes.
# - StableLM will refuse to participate in anything that could harm a human.
# """

# # This will wrap the default prompts that are internal to llama-index
# query_wrapper_prompt = PromptTemplate("<|USER|>{query_str}<|ASSISTANT|>")

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

    #Settings.llm = OpenAI(llm_configs= llm_configs)
    #Settings.llm = Anthropic(model="claude-3-opus-20240229", temperature=0.0)
    Settings.llm = Ollama(model="tinyllama", request_timeout=30.0)

    # Settings.llm = HuggingFaceLLM(
    #     context_window=4096,
    #     max_new_tokens=256,
    #     generate_kwargs={"temperature": 0.7, "do_sample": False},
    #     system_prompt=system_prompt,
    #     query_wrapper_prompt=query_wrapper_prompt,
    #     tokenizer_name="HuggingFaceH4/zephyr-7b-beta",
    #     model_name="HuggingFaceH4/zephyr-7b-beta",
    #     device_map="auto",
    #     stopping_ids=[50278, 50279, 50277, 1, 0],
    #     tokenizer_kwargs={"max_length": 4096},
    #     # uncomment this if using CUDA to reduce memory usage
    #     # model_kwargs={"torch_dtype": torch.float16}
    # )
    
    #Settings.embed_model = OpenAIEmbedding()
    Settings.embed_model= HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.chunk_size = int(os.getenv("CHUNK_SIZE", "1024"))
    Settings.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "20"))
