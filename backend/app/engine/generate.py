from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.core.settings import Settings
from app.engine.constants import STORAGE_DIR
from app.engine.loader import get_documents, get_webpages
from app.settings import init_settings
import logging

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def generate_datasource():
    logger.info("Creating new index")
    # load the documents and create the index
    documents = get_documents()
    #web_documents = get_webpages()

    node_parser = MarkdownElementNodeParser(llm= Settings.llm , num_workers=8)
    nodes = node_parser.get_nodes_from_documents(documents)
    base_nodes, objects = node_parser.get_nodes_and_objects(nodes)

    recursive_index = VectorStoreIndex(nodes=base_nodes+objects)
    #index = VectorStoreIndex.from_documents(documents)

    # store it for later
    #index.storage_context.persist(STORAGE_DIR)
    recursive_index.storage_context.persist(STORAGE_DIR)
    logger.info(f"Finished creating new index. Stored in {STORAGE_DIR}")


if __name__ == "__main__":
    init_settings()
    generate_datasource()
