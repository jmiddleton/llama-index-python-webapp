from llama_index.core.readers import SimpleDirectoryReader
from llama_parse import LlamaParse
from llama_index.readers.web import BeautifulSoupWebReader

DATA_DIR = "data"  # directory containing the documents

parser = LlamaParse(
    #api_key="...",  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown"  # "markdown" and "text" are available
)

def get_documents():
    file_extractor = {".pdf": parser}

    return SimpleDirectoryReader(DATA_DIR, recursive= True, file_extractor=file_extractor).load_data()

def get_webpages():
    loader = BeautifulSoupWebReader()
    return loader.load_data(urls=["http://localhost:3000/doc.html"])