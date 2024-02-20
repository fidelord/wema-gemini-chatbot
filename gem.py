import google.generativeai as genai
import google.ai.generativelanguage as glm

genai.configure(api_key='AIzaSyBni3m6ekzurFIYa1xxVdAXOI-vXAJdcK0')

model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat()

# Initial prompt
messages = [
    {'role':'user', 'parts': ["pretend you are a chatbot named fidel"]},
    {'role':'model','parts':['ok I will do that no problem']},
    {'role':'user','parts':['what is your name?']},

]

response = model.generate_content(messages)

print(response.text)
