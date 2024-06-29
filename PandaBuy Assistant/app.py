from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()
OCTOAI_API_TOKEN = os.getenv("OCTOAI_API_TOKEN")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Setup your LangChain components
url = "https://docs.google.com/spreadsheets/d/1pvudOO35NeYzs0bmn_U0jvTNpSLVXI4feJ1r1aMe644/htmlview"
headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
    ("h4", "Header 4"),
    ("div", "Divider"),
    ("span", "Span")
]

html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
html_header_splits = html_splitter.split_text_from_url(url)
chunk_size = 1024
chunk_overlap = 128
text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
splits = text_splitter.split_documents(html_header_splits)

embeddings = OctoAIEmbeddings(endpoint_url="https://text.octoai.run/v1/")
vector_store = FAISS.from_documents(splits, embedding=embeddings)
retriever = vector_store.as_retriever()

llm = OctoAIEndpoint(
    model="llama-2-13b-chat-fp16",
    max_tokens=1024,
    presence_penalty=0,
    temperature=0.1,
    top_p=0.9,
    api_key=OCTOAI_API_TOKEN
)

template = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:"""
prompt = ChatPromptTemplate.from_template(template)
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    if question:
        answer = chain.invoke(question)
        return jsonify({'answer': answer})
    return jsonify({'error': 'No question provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
