
# def complaints(complaints_query=question):
    
#     complaints_url = "https://drive.google.com/file/d/1AlUXgJoRmNqQJr9tLE0mr5DazH5Bp7ez/view?usp=drive_link"

#     # Return the response from Azure Cognitive Search
#     return  json.dumps(complaints_url)

import json 

question = input("Enter your query here : ")
def complaints(complaints_query=question):
    
    complaints_url = "https://drive.google.com/file/d/1AlUXgJoRmNqQJr9tLE0mr5DazH5Bp7ez/view?usp=drive_link"

    # Return the response from Azure Cognitive Search
    return  json.dumps({"Lodge your complaint using this link":complaints_url, "complaints_query": complaints_query})