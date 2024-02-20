import google.ai.generativelanguage as glm


CombinedTool = glm.Tool(function_declarations=[
    glm.FunctionDeclaration(
        name='Knowledge_base',
        description="This tool should be used to answer questions relating to wema bank such as wema products and other relevant questions. if the answer is not found using this tool the user should be told that there is no information available.",
        parameters=glm.Schema(
            type=glm.Type.OBJECT,
            properties={
                'enquiry_query': glm.Schema(type=glm.Type.STRING,description ="User question about information in knowledge base (ALAT, Loans, USSD) e.g What is ALAT, ussd codes for airtime e.t.c this takes general questions related to wema bank and its products ")
            },
            required=['enquiry_query']
        )
    ),
    
    glm.FunctionDeclaration(
        name='complaints',
        description="Get response from the function 'complaints' when the user have complaints.",
        parameters=glm.Schema(
            type=glm.Type.OBJECT,
            properties={
                'complaints_query': glm.Schema(type=glm.Type.STRING,description ="User question information in relating to complaints e.g 'I have issuess with my accounts', 'I want to lodge a complaint' ")
            },
            required=['complaints_query']
        )
      )

])