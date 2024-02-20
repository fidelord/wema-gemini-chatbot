import sqlite3
import json
import requests
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

def Check_balance(email):
    # Connect to the SQLite database
    conn = sqlite3.connect('bank_database2.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Fetch the account balance based on the email
    cursor.execute("SELECT account_balance FROM customers WHERE email = ?", (email,))
    balance = cursor.fetchone()

    # Check if the email exists in the database
    if balance is not None:
        return json.dumps(f"Account Balance for {email}: ${balance[0]}")
    else:
        return json.dumps(f"Invalid email: {email}")


def complaints(complaints_query):
    
    complaints_url = "https://wemabank.com/complaints"

    # Return the response from Azure Cognitive Search
    return  json.dumps({"Lodge your complaint using this link":complaints_url, "complaints_query": complaints_query})

def Knowledge_base(enquiry_query):
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key='AIzaSyBni3m6ekzurFIYa1xxVdAXOI-vXAJdcK0')
    raw_documents = TextLoader('WemaBank_FAQs_Knowledge_Base.txt').load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)
    db = Chroma.from_documents(documents, embeddings)
    docs = db.similarity_search(enquiry_query)
    return docs[0].page_content

def Top_up_Airtime(service_provider, amount):
    service_provider_list= ['MTN','AIRTEL','GLO','ETISALAT']
    service_provider= service_provider.upper()
    service_provider_flag = 0
    amount = amount

    if service_provider.upper() in service_provider_list:
        service_provider_flag = 1
        return json.dumps("The transaction request was successful")
    else:
        return json.dumps("The Service provider you chose is not available")
    


def handle_unknown_query(unknown_query):
    """
    This function handles unknown user queries.
    The user's query that is not recognized as coginitive or url"
    """
    
    # return json.dumps(f"Sorry, I don't understand the query: {unknown_query}")
    return json.dumps({'unknown': str("'I CAN'T ANSWER")})


def Check_Token(email,token):
     # Connect to the SQLite database
    conn = sqlite3.connect('bank_database2.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Fetch the account balance based on the email
    cursor.execute("SELECT token FROM customers WHERE email = ?", (email,))
    user = cursor.fetchone()

    # Check if the email exists in the database
    if user is not None:
        print(user)
        token2 = user[0]
        if token2 == int(token):
            return json.dumps(f"The authentication was successful")
        else:
            return json.dumps(f"The authentication was not successful maybe your token is incorrect")
    else:
        return json.dumps(f"Invalid email: {email}")
    


