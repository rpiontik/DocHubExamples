# Данные учётки из ЛК разработчика в Сбере

client_id = "client_id"
scope = "GIGACHAT_API_PERS"
client_secret = "client_secret"
auth_data = "auth_data"

from langchain_community.chat_models.gigachat import GigaChat

from langchain.schema import HumanMessage

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from langchain_community.document_loaders import GitLoader

from langchain_core.prompts import PromptTemplate

from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.gigachat import GigaChatEmbeddings

from langchain.chains import RetrievalQA

def create_llm():
    llm = GigaChat(credentials=auth_data, verify_ssl_certs=False)
    return llm

def load_dochub_repo():
    loader = GitLoader(
        #repo_path="./dochub",
        repo_path="./dochub",
        file_filter=lambda file_path: file_path.endswith(".md"),
        branch="master",
    )
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    documents = text_splitter.split_documents(documents)
    print(f"Завершил загрузку документов из DocHub: {len(documents)}")
    return documents

def get_embeddings():
    embeddings = GigaChatEmbeddings(
        credentials=auth_data, verify_ssl_certs=False
    )
    return embeddings

def create_db(documents, embeddings):
    db = Chroma.from_documents(
        documents,
        embeddings,
        client_settings=Settings(anonymized_telemetry=False),
    )
    return db

def make_prompt():
    prompt_template = """Ты сотрудник компании. Отвечай на вопросы, используя the {context}.
    Если ответ найден, дай полный ответ вместе с заголовком документа, из которого была получена информация. Если ответ не найден, то предложить пользователю уточнить свой вопрос или сообщить, что информации по данному вопросу нет в базе данных."""

    prompt = PromptTemplate(input_variables=["context","question"], template=prompt_template)
    return prompt

def create_qa_chain(documents):
    llm = create_llm()
    embeddings = get_embeddings()
    db = create_db(documents, embeddings)
    prompt = make_prompt()
    qa_chain = RetrievalQA.from_chain_type(
        llm, 
        retriever=db.as_retriever(),
        return_source_documents=True,
#        chain_type_kwargs={"prompt": prompt}
    )
    retriever = db.as_retriever()
    return qa_chain, retriever

def question_ai(qa_chain, retriever, question):
    response = qa_chain({"question": question})
    return response