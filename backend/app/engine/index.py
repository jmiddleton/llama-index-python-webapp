import logging
import os

from app.engine.constants import STORAGE_DIR
from llama_index.core.storage import StorageContext
from llama_index.core.indices import load_index_from_storage

logger = logging.getLogger("uvicorn")

def get_index(folder:str = STORAGE_DIR):
    # check if storage already exists
    if not os.path.exists(folder):
        raise FileNotFoundError(
            "StorageContext is empty - call 'python app/engine/generate.py' to generate the storage first"
        )

    # load the existing index
    logger.info(f"Loading index from {folder}...")
    storage_context = StorageContext.from_defaults(persist_dir=folder)

    logger.info(f"Finished loading index from {folder}")
    return load_index_from_storage(storage_context)