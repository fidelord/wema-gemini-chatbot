from openai import AzureOpenAI
import requests
import json
from tools import tools_listing
# from urls import urls_to_scrape
import sqlite3
import requests
from openai import AzureOpenAI
# from extract import extract_information_from_url
from prompts import system_message

azure_openai_endpoint = "https://tunji-service.openai.azure.com/openai/deployments/tunji-model/chat/completions?api-version=2023-07-01-preview"
azure_openai_api_key = "1c5f09b472cd44cf8d28542f9ae25c03"
azure_openai_api_version = "2023-05-15"

client = AzureOpenAI(
    azure_endpoint="https://tunji-service.openai.azure.com",
    api_key="1c5f09b472cd44cf8d28542f9ae25c03",
    api_version="2023-07-01-preview"
)

question = input("Enter your query here : ")



def Check_balance(email=question):
    # Connect to the SQLite database
    conn = sqlite3.connect('bank_database.db')

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


def complaints(complaints_query=question):
    
    complaints_url = "https://drive.google.com/file/d/1AlUXgJoRmNqQJr9tLE0mr5DazH5Bp7ez/view?usp=drive_link"

    # Return the response from Azure Cognitive Search
    return  json.dumps({"Lodge your complaint using this link":complaints_url, "complaints_query": complaints_query})

def knowledge_base(enquiry_query=question):
    
     # Azure Cognitive Search configuration
    search_service_name = "tunji-ai-search-3"
    search_api_key = "nsWEQDTKDiP9ZTXpt3z6Z2nm7IAtcvCyhKOk6Fgh5YAzSeDNAPiy"
    index_name = "yes"
    # api_version = "2023-11-01"
    api_version = "2023-07-01-preview"

    search_url = f"https://{search_service_name}.search.windows.net/indexes/{index_name}/docs?api-version={api_version}"
    headers = {"Content-Type": "application/json", "api-key": search_api_key}

    # Make a request to Azure Cognitive Search
    response = requests.get(search_url, headers=headers, params={"search": enquiry_query})

    # Return the response from Azure Cognitive Search
    return  json.dumps(response.json()['value'][0]['content'])

def top_up_airtime(service_provider= question, amount=question):
    service_provider_list= ['MTN','AIRTEL','GLO','ETISALAT']
    service_provider= service_provider.upper()
    service_provider_flag = 0
    amount = amount

    if service_provider.upper() in service_provider_list:
        service_provider_flag = 1
        return json.dumps("The transaction request was successful")
    else:
        return json.dumps("The Service provider you chose is not available")
    


def handle_unknown_query(unknown_query=question):
    """
    This function handles unknown user queries.
    The user's query that is not recognized as coginitive or url"
    """
    
    # return json.dumps(f"Sorry, I don't understand the query: {unknown_query}")
    return json.dumps({'unknown': str("'I CAN'T ANSWER")})


def check_token(email,token):
     # Connect to the SQLite database
    conn = sqlite3.connect('bank_database.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Fetch the account balance based on the email
    cursor.execute("SELECT * FROM customers WHERE email = ?", (email,))
    user = cursor.fetchone()

    # Check if the email exists in the database
    if user is not None:
        token2 = user[0][-1]
        if token2 == token:
            return json.dumps(f"The authentication was successful")
        else:
            return json.dumps(f"The authentication was not successful maybe your token is incorrect")
    else:
        return json.dumps(f"Invalid email: {email}")
    



def run_conversation():
    # Step 1: send the conversation and available functions to the model
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": question}
    ]
    tools = tools_listing
    response = client.chat.completions.create(
        model="tunji-model",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    print(tool_calls, "\n")

    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            
            
            # "handle_unknown_query": handle_unknown_query,
            "complaints":complaints,
            "Check_balance":Check_balance,
            "knowledge_base":knowledge_base,
            "top_up_airtime": top_up_airtime,
            "handle_unknown_query": handle_unknown_query

            
        }  # Available functions

        messages.append(response_message)  # extend conversation with assistant's reply

        # Move the assignment of function_name before the conditional checks
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            
            if function_name == "knowledge_base":
                function_response = function_to_call(
                    enquiry_query=function_args.get("enquiry_query"),
                   
                )
            elif function_name == "Check_balance":
                function_response = function_to_call(
                    email=function_args.get("email"),
                    
                   
                )
            # elif function_name == "handle_unknown_query":
            #     function_response = function_to_call(
            #         unknown_query=function_args.get("unknown_query"),
                   
            #     )
            elif function_name == "complaints":
                function_response = function_to_call(
                    complaints_query=function_args.get("complaints_query"),
                   
                )  

            elif function_name == "top_up_airtime":
                function_response = function_to_call(
                    service_provider=function_args.get("service_provider"),
                    amount=function_args.get("amount"),
                                    
                   
                )

            elif function_name == None:
                function_response = function_to_call(
                    unknown_query=function_args.get("unknown_query"),
                    
                
                )               
                          

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

        # Step 4: send the info for each function call and function response to the model
        second_response = client.chat.completions.create(
            model="tunji-model",
            messages=messages,
        )

        return print(second_response.choices[0].message.content)

run_conversation()