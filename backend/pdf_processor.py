from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import FAISS
#from langchain.vectorstores import Chroma #vector store
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from langchain.chains import (
    StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
)
from langchain.llms import Bedrock
from langchain.embeddings import BedrockEmbeddings
import boto3

load_dotenv()  # This loads the environment variables from a .env file

# Global variable to hold the initialized QA chain
qa_chain = None
# Instead of hardcoding the keys, use environment variables
cohere_api_key = os.getenv('COHERE_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

#aws set up
aws_region = 'us-west-2'
aws_service = 'bedrock'
aws_cli_profile_name = 'raybdr'
session = boto3.Session(profile_name=aws_cli_profile_name)
bedrock_client = session.client(service_name='bedrock', region_name=aws_region, endpoint_url='https://bedrock-runtime.'+aws_region+'.amazonaws.com')
#bedrock_client = boto3.client("bedrock-runtime", region_name=aws_region)
#bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name=aws_region, aws_access_key_id='AKIAZPHR3E6TCB7R35MM', aws_secret_access_key='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',)


def initialize_qa_system(pdf_directory):

    global qa_chain
    # Load PDF documents
    loader = PyPDFDirectoryLoader(pdf_directory)
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # Generate embeddings for document chunks
    #embeddings = CohereEmbeddings(model="multilingual-22-12", cohere_api_key=cohere_api_key)
    embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1",
                                       client=bedrock_client)
    #doc_search = Chroma.from_documents(docs, embeddings)
    vectorstore_faiss = FAISS.from_documents(docs, embeddings)

    # Initialize the language model
    #llm = OpenAI(api_key=openai_api_key)
    llm = Bedrock(model_id="anthropic.claude-v2", client=bedrock_client, model_kwargs={"max_tokens_to_sample": 1000})
    # conversation history  needs to be added later
    # Create a custom prompt template
    prompt_template_qa = PromptTemplate(
    template="""Text: {context}\n\nQuestion: {question}\n\nAnswer the question based on the text provided. If the text doesn't contain the answer, reply that the answer is not available.\n\n""",
    input_variables=["context", "question"]
    )


    # Set up the question-answering chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore_faiss.as_retriever(),
        chain_type_kwargs={"prompt": prompt_template_qa},
        return_source_documents=True
     )



def ask_question(query):
    if qa_chain is None:
        return "QA system is not initialized.", None
    answer = qa_chain({"query": query})
    result = answer["result"].replace("\n", "").replace("Answer:", "").strip()
    # citation
    document = answer['source_documents'][-1]  # This is the last document in the list
    # source_directory = document.metadata['source']  # Extracting the 'source' from metadat
    original_path = document.metadata['source']  # This is 'pdf_directory/YourDocument.pdf'
    file_name = os.path.basename(original_path)  # This extracts 'YourDocument.pdf' from the path

    return result
