from flask import Flask, render_template, request, jsonify 
from Gemini_Agent import Smart_Agent
from main_function import available_functions,PERSONA
app = Flask(__name__) 
agent = Smart_Agent(persona=PERSONA,functions_list=available_functions)


Conversation=[{'role':'user','parts':[PERSONA]},{'role':'model','parts':'ok I will do my best to follow the above instructions carefully.'}]
print(Conversation)

def get_completion(prompt):
	stream_out,  history, agent_response = agent.run(user_input=prompt, conversation=Conversation, stream=False)
	response = agent_response
	Conversation.append({"role":"user", "parts":[prompt]})
	Conversation.append({"role":"model", "parts":[response]})
	#print(len(Conversation))
	return response 

@app.route("/", methods=['POST', 'GET']) 
def query_view(): 
	if request.method == 'POST': 
		print('step1') 
		prompt = request.form['prompt'] 
		response = get_completion(prompt) 
		print(response) 

		return jsonify({'response': response}) 
	return render_template('index.html') 



if __name__ == "__main__": 
	app.run(debug=True) 
