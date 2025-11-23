# tools.py

from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever,MultiQueryRetriever


from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pickle
from langchain_core.tools import Tool
import os
import sys

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


base_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(base_dir, 'all_chunk_data.pkl')
db_path = os.path.join(base_dir, "rag_db")

all_chunk = []

try:
    with open(file_path, 'rb') as file:
        all_chunk = pickle.load(file)
    print(f"✅ File uploaded successfully: {file_path}")
except FileNotFoundError:
    
    error_msg = f"❌ CRITICAL ERROR: Pickle file not found! Searched location: {file_path}"
    print(error_msg)
    raise FileNotFoundError(error_msg)
    


DB_path = "rag_db"
vector_db = Chroma(
    persist_directory = DB_path,
    embedding_function = embedding_model
)

prompt_template_string = """
CONTEXT:
{context}

QUESTION:
{question}

INSTRUCTIONS:
Act as a helpful expert. Provide a clear and direct answer to the question using only the information in the context.
- You can perform simple calculations like unit conversions (e.g., pounds to kg) to make the answer more helpful.
- If the answer is not in the context, state that the document does not contain this information.
- Answer directly without starting your response with "Based on the context....
"""

custom_prompt = PromptTemplate(
    template = prompt_template_string,
    input_variables = ['context', 'question']
)

bm25_retriver = BM25Retriever.from_documents(
    documents=all_chunk
)

bm25_retriver.k = 7

similarity_retriever = vector_db.as_retriever(
    search_type = "similarity",
    search_kwargs = {'k':7}
)

ensemble_retriver = EnsembleRetriever(
    retrievers = [bm25_retriver,similarity_retriever],
    weights = [0.3,0.7]
)
multiquery_esemble_retriever = MultiQueryRetriever.from_llm(
    llm = llm, 
    retriever = ensemble_retriver
)


rag_chain = RetrievalQA.from_chain_type(
    llm = llm,
    chain_type = 'stuff',
    retriever = multiquery_esemble_retriever,
    chain_type_kwargs = {"prompt": custom_prompt},
    return_source_documents = True
)

rag_tool = Tool(
    name = "DocumentSearch",
    func = rag_chain.invoke,
    description = "Use this tool to answer questions about Large Language Model (LLM) agents. It searches a collection of academic papers on topics like tool use, RAG, planning, memory, and feedback learning."
)


search_runnable = TavilySearch(max_results = 5)

tools = [search_runnable, rag_tool]