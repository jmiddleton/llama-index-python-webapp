import logging
import os

from app.engine.constants import STORAGE_DIR
from llama_index.core.storage import StorageContext
from llama_index.core.indices import load_index_from_storage

logger = logging.getLogger("uvicorn")

cached_index= None

def get_index():
    # check if storage already exists
    if not os.path.exists(STORAGE_DIR):
        raise Exception(
            "StorageContext is empty - call 'python app/engine/generate.py' to generate the storage first"
        )

    # load the existing index
    logger.info(f"Loading index from {STORAGE_DIR}...")
    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)

    global cached_index
    if cached_index == None:
        logger.info(f"No cached index, loading from storage...")
        cached_index = load_index_from_storage(storage_context)

    logger.info(f"Finished loading index from {STORAGE_DIR}")
    return cached_index