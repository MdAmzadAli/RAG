# from unstructured.partition.auto import partition
# from unstructured.documents.elements import Element

# def parse_file(file_path:str)-> list[Element]:
#     elements: list[Element] = partition(file_path)
#     return [el.text for el in elements if el.text and el.text.strip()]

from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def parse_file(file_path:str):
    loader= UnstructuredFileLoader(file_path)
    doc= loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(doc)
    texts = [doc.page_content for doc in chunks]
    return texts


