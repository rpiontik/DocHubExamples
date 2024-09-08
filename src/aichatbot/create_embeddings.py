import logging

from langchain_community.vectorstores import Chroma
from chromadb.config import Settings

from langchain_community.document_loaders import GitLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from yandex_chain import YandexEmbeddings

from yandex_iam import get_iam_token

import yaml
import os

logging.basicConfig(
    filename="create_embeddings.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def load_dochub_documents():
    os.chdir("./dochub")
    os.system("git config core.filemode false")
    os.system("git pull")
    loader = GitLoader(
        repo_path="./docs",
        #repo_path="/Users/dmitrytimoshenko/Desktop/projects/tokeon/gitlab/dochub",
        file_filter=lambda file_path: file_path.endswith(".md"),
        branch="master",
    )
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    documents = text_splitter.split_documents(documents)
    logging.info(f"Завершил загрузку документов из DocHub: {len(documents)}")
    os.chdir("..")
    return documents

def create_embeddings(documents, folder_id, iam_token, collection_name):
    embeddings = YandexEmbeddings(folder_id= folder_id, iam_token=iam_token)
    logging.info("Инициализировал YandexEmbeddings")
    logging.info("Создаю коллекцию ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents,
        embeddings,
        client_settings=Settings(anonymized_telemetry=False, persist_directory="./chroma_db", is_persistent = True),
        persist_directory="./chroma_db", 
        collection_name=collection_name
    )
    vectorstore.persist()
    logging.info("Создал коллекцию ChromaDB")
    return vectorstore

def create_embeddings_dochub():
    iam_token = get_iam_token()
    logging.info("Загружаю документы")
    dochub_docs = load_dochub_documents()
    logging.info(f"Загрузил документы DocHub: {len(dochub_docs)}")
    with open("bot_config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    folder_id = config["folder_id"]
    logging.info("Запустил создание коллекции эмбеддингов...")
    create_embeddings(dochub_docs, folder_id, iam_token, "dochub")
    logging.info("Коллекция эмбеддингов создана")

create_embeddings_dochub()