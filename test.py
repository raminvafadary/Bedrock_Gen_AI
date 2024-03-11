import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import Bedrock
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import BedrockEmbeddings
import boto3


#load pdfs
loader = PyPDFDirectoryLoader("./pdf_directory")
documents = loader.load()


# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)
#aws set up
aws_region = 'us-west-2'
aws_service = 'bedrock'
aws_cli_profile_name = 'raybdr'
#session = boto3.Session(profile_name=aws_cli_profile_name)
#bedrock_client = session.client(service_name='bedrock', region_name=aws_region, endpoint_url='https://bedrock-runtime.'+aws_region+'.amazonaws.com')
session = boto3.Session()
bedrock_client = session.client('bedrock',region_name=aws_region)

#enbeddings
embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1",
                                       client=bedrock_client)
                                     
print(embeddings.embed_query("This is a content of the document"))
# #vectordb
# vectorstore_faiss = FAISS.from_documents(docs, embeddings)

# #llm call
# llm = Bedrock(model_id="anthropic.claude-v2", client=bedrock_client, model_kwargs={"max_tokens_to_sample": 1000})

# #prompt
# prompt_template_qa = PromptTemplate(
#     template="""Text: {context}\n\nQuestion: {question}\n\nAnswer the question based on the text provided. If the text doesn't contain the answer, reply that the answer is not available.\n\n""",
#     input_variables=["context", "question"]
#     )

# #QA
# # Set up the question-answering chain
# qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=vectorstore_faiss.as_retriever(),
#         chain_type_kwargs={"prompt": prompt_template_qa},
#         return_source_documents=True
#      )

# query="why??"
# answer = qa_chain({"query": query})
# result = answer["result"].replace("\n", "").replace("Answer:", "").strip()
# print(result)
