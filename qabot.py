import os
from dotenv import load_dotenv

# Memuat variabel dari file .env
load_dotenv()

from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from ibm_watsonx_ai import Credentials
from langchain_ibm import WatsonxLLM, WatsonxEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
import gradio as gr

# Mengabaikan pesan peringatan agar output terminal bersih
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
warnings.filterwarnings('ignore')

# ---------------------------------------------------------
# KREDENSIAL DIKAMALKAN DARI FILE .ENV
# ---------------------------------------------------------
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
API_KEY = os.getenv("WATSONX_APIKEY")
URL = "https://us-south.ml.cloud.ibm.com"

## Tugas 1: Document loader
def document_loader(file):
    loader = PyPDFLoader(file)
    loaded_document = loader.load()
    return loaded_document

## Tugas 2: Text splitter
def text_splitter(data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )
    chunks = text_splitter.split_documents(data)
    return chunks

## Tugas 3: Embedding model
def watsonx_embedding():
    embed_params = {
        EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3
    }
    watsonx_embedding_obj = WatsonxEmbeddings(
        model_id="ibm/slate-125m-english-rtrvr-v2",
        url=URL,
        project_id=PROJECT_ID,
        params=embed_params,
        apikey=API_KEY
    )
    return watsonx_embedding_obj

## Tugas 4: Vector db
def vector_database(chunks):
    embedding_model = watsonx_embedding()
    vectordb = Chroma.from_documents(chunks, embedding_model)
    return vectordb

## Tugas 5: Retriever
def retriever(file):
    splits = document_loader(file)
    chunks = text_splitter(splits)
    vectordb = vector_database(chunks)
    retriever_obj = vectordb.as_retriever()
    return retriever_obj

## LLM (Menggunakan model Mixtral sesuai instruksi tugas)
def get_llm():
    model_id = 'mistralai/mixtral-8x7b-instruct-v01'
    parameters = {
        GenParams.TEMPERATURE: 0.5,
        GenParams.MAX_NEW_TOKENS: 256,
    }
    watsonx_llm = WatsonxLLM(
        model_id=model_id,
        url=URL,
        project_id=PROJECT_ID,
        params=parameters,
        apikey=API_KEY
    )
    return watsonx_llm

## Tugas 6: QA Chain
def retriever_qa(file, query):
    try:
        from langchain_classic.chains import RetrievalQA
    except ImportError:
        try:
            from langchain.chains import RetrievalQA
        except ImportError:
            from langchain.chains.retrieval_qa.base import RetrievalQA
            
    llm = get_llm()
    retriever_obj = retriever(file)
    qa = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever_obj, 
        return_source_documents=False
    )
    response = qa.invoke(query)
    return response['result']

# Create Gradio interface
rag_application = gr.Interface(
    fn=retriever_qa,
    inputs=[
        gr.File(label="Upload PDF File", file_count="single", file_types=['.pdf'], type="filepath"),
        gr.Textbox(label="Input Query", lines=2, placeholder="Apa yang dibicarakan dalam makalah ini?")
    ],
    outputs=gr.Textbox(label="Answer"),
    title="Quest Analytics QA Bot",
    description="Upload a PDF document and ask any question. The chatbot will try to answer using the provided document."
)

# Launch the app
if __name__ == "__main__":
    rag_application.launch(server_name="127.0.0.1", server_port=7860)