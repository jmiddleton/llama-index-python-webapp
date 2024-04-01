import os
from app.engine.index import get_index
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker

top_k = os.getenv("TOP_K", 3)

reranker = FlagEmbeddingReranker(
    top_n=int(top_k),
    model="BAAI/bge-reranker-large",
)

recursive_chat_engine = None
recursive_query_engine = None

def get_chat_engine():
    system_prompt = os.getenv("SYSTEM_PROMPT")

    global recursive_chat_engine
    if recursive_chat_engine == None:
        recursive_chat_engine = get_index().as_chat_engine(
            similarity_top_k=5,
            system_prompt=system_prompt,
            node_postprocessors=[reranker],
            chat_mode="condense_plus_context",
            verbose=True
        )

    return recursive_chat_engine

def get_query_engine():

    global recursive_query_engine
    if recursive_query_engine == None:
        recursive_query_engine = get_index().as_query_engine(
            similarity_top_k=15,
            node_postprocessors=[reranker],
            verbose=True
        )

    return recursive_query_engine
