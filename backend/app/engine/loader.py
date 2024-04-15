from llama_index.core.readers import SimpleDirectoryReader
from llama_parse import LlamaParse
from llama_index.readers.web import BeautifulSoupWebReader

DATA_DIR = "data"  # directory containing the documents

parser = LlamaParse(
    result_type="markdown"  # "markdown" and "text" are available
)

def get_documents(folder:str = DATA_DIR):
    #file_extractor = {".pdf": parser}

    return SimpleDirectoryReader(folder, recursive= True).load_data()

def get_webpages():
    loader = BeautifulSoupWebReader()
    return loader.load_data(urls=["http://localhost:3000/doc.html"])