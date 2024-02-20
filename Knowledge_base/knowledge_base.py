import requests
import json

question = input("Enter your query here : ")

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