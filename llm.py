import os
import logging
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_groq import ChatGroq

# Optional: prevent Streamlit from rerunning on save
os.environ["STREAMLIT_SERVER_RUN_ON_SAVE"] = "false"

# Load environment variables
load_dotenv()
logging.basicConfig(level=logging.INFO)

# Constants
PDF_DIR = "data"
FAISS_DIR = "faiss_index"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

def load_pdf(path=PDF_DIR):
    """Load PDF documents from a directory."""
    loader = DirectoryLoader(path, glob="*.pdf", loader_cls=PyPDFLoader)
    return loader.load()

def create_chunks(docs):
    """Split documents into text chunks for vector embedding."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(docs)

def get_embedding_model():
    """Return HuggingFace embedding model."""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_vector_store(chunks, embedding_model, persist_directory=FAISS_DIR):
    """Create and persist a FAISS vector store."""
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local(persist_directory)
    return vectorstore

def get_vector_store():
    """Load existing or create new FAISS vector store."""
    embedding_model = get_embedding_model()
    if os.path.exists(os.path.join(FAISS_DIR, "index.faiss")):
        logging.info("Loading existing FAISS vector store...")
        return FAISS.load_local(FAISS_DIR, embedding_model)
    else:
        logging.info("Creating new FAISS vector store from PDFs...")
        documents = load_pdf()
        chunks = create_chunks(documents)
        return create_vector_store(chunks, embedding_model)

def get_llm():
    """Initialize Groq LLM."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY in .env file")

    return ChatGroq(
        temperature=0.3,
        groq_api_key=api_key,
        model_name=GROQ_MODEL,
        max_tokens=1024
    )

def run_llm(prompt):
    """Run the Groq LLM with MultiQueryRetriever and FAISS."""
    llm = get_llm()
    vector_store = get_vector_store()

    retriever = MultiQueryRetriever.from_llm(
        retriever=vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3}),
        llm=llm,
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )

    return qa_chain.invoke({"query": prompt})

def print_sources(source_docs):
    """Print source documents used in the response."""
    for doc in source_docs:
        source = doc.metadata.get("source", "Unknown source")
        content = doc.page_content[:300].replace("\n", " ")
        print(f"- {source}: {content}...")
