import os
import time
import tempfile
from dotenv import load_dotenv
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# Load dotenv file
load_dotenv()

# Langsmith tracking
os.environ['LANGSMITH_API_KEY'] = os.getenv('LANGSMITH_API_KEY')
os.environ['LANGSMITH_TRACING'] = os.getenv('LANGSMITH_TRACING')
os.environ['LANGSMITH_ENDPOINT'] = os.getenv('LANGSMITH_ENDPOINT')
os.environ['LANGSMITH_PROJECT'] = os.getenv('LANGSMITH_PROJECT')


def load_pdf(uploaded_file):
    if uploaded_file:
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(uploaded_file.read())
                pdf_path = temp_pdf.name  # Get the temporary file path

            # Load the PDF using PyPDFLoader
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            return documents

def split_docs(chunk_size, chunk_overlap, docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    split_docs = text_splitter.split_documents(docs)
    return split_docs

def create_embeddings(model_name):
    return OllamaEmbeddings(model=model_name)

def create_vectorstores(split_docs, embeddings):
    faiss_db = FAISS.from_documents(split_docs, embeddings)
    return faiss_db

def create_llm(model_name):
    llm = OllamaLLM(model=model_name)
    return llm

def create_chat_prompt_template(prompt_template):
    return ChatPromptTemplate.from_template(prompt_template)

def create_stuff_docs_chain(llm, prompt):
    return create_stuff_documents_chain(llm, prompt)

def create_retriever(faiss_db):
    return faiss_db.as_retriever(search_kwargs={"k":3})

def create_retriever_chain(retriever, stuff_docs_chain):
    return create_retrieval_chain(retriever, stuff_docs_chain)


if __name__ == "__main__":

    st.set_page_config(
        page_title="Chat With PDF",
        page_icon="🌏",
        # layout="wide",
        # initial_sidebar_state="expanded",
    )

    st.title("Chat with PDF🗃️")

    uploaded_file = st.file_uploader(label="Upload you PDF file", type='pdf', accept_multiple_files=False)

    if 'db' not in st.session_state:
        st.session_state.db = None

    if 'retriever_chain' not in st.session_state:
        st.session_state.retriever_chain = None

    if 'output' not in st.session_state:
        st.session_state.output = None

    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    if uploaded_file:

        pdf_file = load_pdf(uploaded_file)

        if st.session_state.db is None:
            with st.spinner("Splitting the documents into chunks..."):
               
                split_document_texts = split_docs(chunk_size=500, chunk_overlap=100, docs=pdf_file)

            with st.spinner("Create vector data store..."):
                embeddings = create_embeddings(model_name="nomic-embed-text")
                st.session_state.db = create_vectorstores(split_document_texts, embeddings)

            # st.success("Document processed and vector database created!")

            llm = create_llm(model_name="phi3:mini")
           
            
            prompt_template = """
You are an AI assistant that answers questions using ONLY the provided document context.

<context>
{context}
</context>

Question: {input}

Provide a clear and accurate answer based only on the context above.
"""

            prompt = create_chat_prompt_template(prompt_template)
            stuff_docs_chain = create_stuff_docs_chain(llm, prompt)
            retriever = create_retriever(st.session_state.db)
            st.session_state.retriever_chain = create_retriever_chain(retriever, stuff_docs_chain)

    if st.session_state.retriever_chain:
        user_input = st.text_area(label='Ask Your Question Related to Uploaded Document', value=st.session_state.user_input)

        col1, col2 = st.columns(2)

        submit_btn = col1.button("Submit")
        reset_btn = col2.button("Reset")

        if submit_btn:
            if user_input:
                response = st.session_state.retriever_chain.invoke({'input': str(user_input)})
                st.session_state.output = response['answer']
                st.session_state.user_input = user_input

            else:
                st.warning("Please enter you question before clicking Submit button.")

        if reset_btn:
            st.session_state.output = None
            st.session_state.user_input = ""

        if st.session_state.output:
            st.write(f"**Answer:** {st.session_state.output}")






