import google.generativeai as genai
import google.ai.generativelanguage as glm
from Gemini_Agent import Smart_Agent
from main_function import available_functions,PERSONA
agent = Smart_Agent(persona=PERSONA,functions_list=available_functions)
Conversation=[{'role':'user','parts':[PERSONA]},{'role':'model','parts':['ok I will do my best']}]
prompt ='What is your name'
stream_out, history, agent_response = agent.run(user_input=prompt, conversation=Conversation, stream=False)
print(agent_response)