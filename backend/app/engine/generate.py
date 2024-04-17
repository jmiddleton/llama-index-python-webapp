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
from app.engine.constants import STORAGE_DIR, DATA_DIR
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
    # load the documents and create the index
    for i in range(1, 4):
        logger.info(f"Creating new index for {DATA_DIR + str(i)}...")
        documents = get_documents(DATA_DIR + str(i))
        
        nodes = node_parser.get_nodes_from_documents(documents)
        leaf_nodes = get_leaf_nodes(nodes)

        storage_context = StorageContext.from_defaults()
        storage_context.docstore.add_documents(nodes)

        index = VectorStoreIndex(
            leaf_nodes, storage_context=storage_context
        )

        # store it for later
        index.storage_context.persist(STORAGE_DIR + str(i))
        logger.info(f"Finished creating new index. Stored in {STORAGE_DIR + str(i)}")


if __name__ == "__main__":
    init_settings()
    generate_datasource()
