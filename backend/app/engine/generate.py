from dotenv import load_dotenv
from llama_index.core import (
    ServiceContext,
    StorageContext,
    VectorStoreIndex
)
from llama_index.core.node_parser import (
    HierarchicalNodeParser,
    get_leaf_nodes,
    MarkdownElementNodeParser
)
from llama_index.core.settings import Settings
from app.engine.constants import STORAGE_DIR
from app.engine.loader import get_documents, get_webpages
from app.settings import init_settings
import logging

# create the hierarchical node parser w/ default settings
node_parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128]
)

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def generate_datasource():
    logger.info("Creating new index")
    # load the documents and create the index
    documents = get_documents()
    #web_documents = get_webpages()

    
    nodes = node_parser.get_nodes_from_documents(documents)
    leaf_nodes = get_leaf_nodes(nodes)

    storage_context = StorageContext.from_defaults()
    storage_context.docstore.add_documents(nodes)

    index = VectorStoreIndex(
        leaf_nodes, storage_context=storage_context
    )

    # node_parser = MarkdownElementNodeParser(llm= Settings.llm , num_workers=4)
    # nodes = node_parser.get_nodes_from_documents(documents)
    # base_nodes, objects = node_parser.get_nodes_and_objects(nodes)

    #index = VectorStoreIndex(nodes=base_nodes+objects)

    # store it for later
    index.storage_context.persist(STORAGE_DIR)
    logger.info(f"Finished creating new index. Stored in {STORAGE_DIR}")


if __name__ == "__main__":
    init_settings()
    generate_datasource()
