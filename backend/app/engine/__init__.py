import os
from app.engine.index import get_index
from app.engine.constants import STORAGE_DIR
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.core.settings import Settings
# from llama_index.core.query_engine import RouterQueryEngine
# from llama_index.core.selectors import LLMSingleSelector
# from llama_index.core.query_engine import SubQuestionQueryEngine
# from llama_index.postprocessor.cohere_rerank import CohereRerank
# COHERE_API_KEY = os.getenv("COHERE_API_KEY")
from app.agents.booking import BookingToolSpec
from llama_index.agent.openai import OpenAIAgent

top_k = os.getenv("TOP_K", 3)

static_descriptions = {
    'data1': 'Provides information about Intelligo (PRTG) troubleshooting guide',
    'data2': 'Provides information about Kailo troubleshooting guide',
    'data3': 'Provides information about Visage HL7 Integration guide'
}

# reranker = FlagEmbeddingReranker(
#     top_n=int(top_k),
#     model="BAAI/bge-reranker-large",
# )
# cohere_rerank = CohereRerank(
#     model='rerank-english-v3.0',
#     api_key=COHERE_API_KEY,
# )
sentence_reranker = SentenceTransformerRerank(
    top_n=3,
    model="BAAI/bge-reranker-base"
)

def get_chat_engine():
    # return get_index(STORAGE_DIR + "0").as_chat_engine(
    #     similarity_top_k=int(top_k),
    #     system_prompt=os.getenv("SYSTEM_PROMPT"),
    #     node_postprocessors=[sentence_reranker],
    #     verbose=True,
    # )
    tool_spec = BookingToolSpec()
    agent = OpenAIAgent.from_tools(tool_spec.to_tool_list(), verbose=True)
    
    return agent

def get_query_engine():
    tool_spec = BookingToolSpec()
    agent = OpenAIAgent.from_tools(tool_spec.to_tool_list())

    return agent

def get_query_engine_bueno():
    query_engine_tools = []

    for i in range(1, 4):
        index = get_index(STORAGE_DIR + str(i))
        automerging_retriever = index.as_retriever(
            similarity_top_k=int(top_k)
        )

        retriever = AutoMergingRetriever(
            automerging_retriever,
            index.storage_context,
            verbose=True
        )

        query_engine = RetrieverQueryEngine.from_args(
            retriever,
            node_postprocessors=[sentence_reranker]
        )

        query_engine_tools.append(
            QueryEngineTool(
                query_engine=query_engine,
                metadata=ToolMetadata(
                    name=f"query_engine_{i}",
                    description=(static_descriptions[f"data{i}"])
                )
            )
        )

    # query_engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=query_engine_tools, use_async=False)

    # query_engine = RouterQueryEngine(
    #     selector=LLMSingleSelector.from_defaults(),
    #     query_engine_tools=query_engine_tools,
    #     verbose=True,
    # )

    agent = ReActAgent.from_tools(query_engine_tools, llm=Settings.llm, verbose=True)

    return agent
