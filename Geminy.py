import google.generativeai as genai
import google.ai.generativelanguage as glm
import json

genai.configure(api_key='AIzaSyBni3m6ekzurFIYa1xxVdAXOI-vXAJdcK0')

calculator = glm.Tool(
    function_declarations=[
      glm.FunctionDeclaration(
        name='add',
        description="Returns the sum of two numbers.",
        parameters=glm.Schema(
            type=glm.Type.OBJECT,
            properties={
                'a': glm.Schema(type=glm.Type.NUMBER),
                'b': glm.Schema(type=glm.Type.NUMBER)
            },
            required=['a','b']
        )
      ),
      glm.FunctionDeclaration(
        name='multiply',
        description="Returns the product of two numbers.",
        parameters=glm.Schema(
            type=glm.Type.OBJECT,
            properties={
                'a':glm.Schema(type=glm.Type.NUMBER),
                'b':glm.Schema(type=glm.Type.NUMBER)
            },
            required=['a','b']
        )
      )
    ])




model = genai.GenerativeModel('gemini-pro', tools=[calculator])
chat = model.start_chat(history=[
    {'role':'user', 'parts': ["pretend you are a chatbot named fidel"]},
    {'role':'model','parts':['ok I will do that no problem']},
   ])



response = chat.send_message("what is 4 multiplied by 8")
argumentas = response.candidates[0].content.parts[0].function_call.args
function_arguments = dict(argumentas)
print(function_arguments)

if response.candidates[0].content.parts[0].function_call:
    print('hell yeah')

fc = response.candidates[0].content.parts[0].function_call
assert fc.name == 'multiply'

result = fc.args['a'] * fc.args['b']

response = chat.send_message(
    glm.Content(
    parts=[glm.Part(
        function_response = glm.FunctionResponse(
          name='multiply',
          response={'result': result}
        )
    )]
  )
)

print(response)
