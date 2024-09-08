from yandex_chain import YandexEmbeddings
from yandex_chain import YandexLLM

from langchain_community.vectorstores import FAISS

from chromadb.config import Settings
from langchain_community.vectorstores import Chroma

from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import GitLoader
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

import logging
import yaml

from yandex_iam import get_iam_token

with open("bot_config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

service_account_id = config["service_account_id"]
api_key_id = config["api_key_id"]
folder_id = config["folder_id"]
service_account_private_key = config["service_account_private_key"]

logging.basicConfig(
    filename="telegram_bot.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def get_retriever(iam_token, collection_name, documents=None):
    logging.info("Создаю эмбеддинги")
    embeddings = YandexEmbeddings(folder_id= folder_id, iam_token=iam_token)
    logging.info("Создал эмбеддинги")
    logging.info(f"Открываю базу данных, коллекцию {collection_name}...")
    vectorstore = Chroma(collection_name=collection_name, persist_directory="./chroma_db", embedding_function=embeddings)
    logging.info("Открыл векторную БД")
    retriever = vectorstore.as_retriever()
    logging.info("Создал Retriever")
    return retriever

def create_llm(iam_token, prompt):
    logging.info("folder_id: "+folder_id)
    llm = YandexLLM(folder_id= folder_id, iam_token=iam_token, model_uri="gpt://{folder_id}/yandexgpt-lite/latest")
    return llm


#def create_qa_chain(documents):
def create_qa_chain(collection_name):
    iam_token = get_iam_token()

    template = """You are company employee. Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    logging.info("Создаю llm_chain...")
    llm = create_llm(iam_token, prompt)
    logging.info("...Создал llm-chain")

    logging.info("Создаю векторную БД...")
    #retriever = get_retriever(iam_token, documents)
    retriever = get_retriever(iam_token, collection_name)

    qa_chain = create_stuff_documents_chain(llm, prompt)

    logging.info("Создал QA chain")

    return qa_chain, retriever

def question_ai(qa_chain, retriever, question):
    #query = "Опиши состояния объекта ЦФА"
    query = question
    docs = retriever.invoke(query)
    #logging.info("Получил документы из ретривера: "+str(docs))
    response = qa_chain.invoke({"query": query, "question": query, 'context': docs})
    #response = qa_chain.invoke({"query": query, "question": query, 'context': docs, 'input_documents': docs})

    logging.info(f" + Answer is: {response}")

    return response