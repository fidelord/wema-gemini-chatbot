from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter


embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key='AIzaSyBni3m6ekzurFIYa1xxVdAXOI-vXAJdcK0')
raw_documents = TextLoader('WemaBank_FAQs_Knowledge_Base.txt').load()
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)
db = Chroma.from_documents(documents, embeddings)
query = "Airtime"
docs = db.similarity_search(query, k=2)
print(docs[0].page_content)
