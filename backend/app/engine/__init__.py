import os
from app.engine.index import get_index
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

top_k = os.getenv("TOP_K", 3)

reranker = FlagEmbeddingReranker(
    top_n=int(top_k),
    model="BAAI/bge-reranker-large",
)

recursive_chat_engine = None
recursive_query_engine = None

def get_chat_engine():
    global recursive_chat_engine
    if recursive_chat_engine == None:
        recursive_chat_engine = get_index().as_chat_engine(
            similarity_top_k=5,
            system_prompt=os.getenv("SYSTEM_PROMPT"),
            node_postprocessors=[reranker],
            chat_mode="condense_plus_context",
            verbose=True
        )

    return recursive_chat_engine

def get_query_engine():

    # global recursive_query_engine
    # if recursive_query_engine == None:
    #     recursive_query_engine = get_index().as_query_engine(
    #         similarity_top_k=15,
    #         node_postprocessors=[reranker],
    #         verbose=True
    #     )

    # return recursive_query_engine

    automerging_retriever = get_index().as_retriever(
        similarity_top_k=6
    )

    retriever = AutoMergingRetriever(
        automerging_retriever, 
        get_index().storage_context, 
        verbose=True
    )

    rerank = SentenceTransformerRerank(top_n=6, model="BAAI/bge-reranker-base")

    auto_merging_engine = RetrieverQueryEngine.from_args(
        retriever, node_postprocessors=[rerank]
    )

    return auto_merging_engine
