import google.generativeai as genai
import google.ai.generativelanguage as glm
import inspect
from Geminy_tools import CombinedTool
genai.configure(api_key='AIzaSyBni3m6ekzurFIYa1xxVdAXOI-vXAJdcK0')

def gpt_stream_wrapper(response):
    for chunk in response:
        chunk_msg= chunk['choices'][0]['delta']
        chunk_msg= chunk_msg.get('content',"")
        yield chunk_msg

class Agent(): #Base class for Agent
    def __init__(self, engine,persona, name=None, init_message=None):
        if init_message is not None:
            init_hist =[{"role":"user", "parts":persona}, {"role":"model", "parts":init_message}]
        else:
            init_hist =[{"role":"user", "parts":persona}]

        self.init_history =  init_hist
        self.persona = persona
        self.engine = engine
        self.name= name
    def generate_response(self, new_input,history=None, stream = False,request_timeout =20,api_version = "2023-05-15"):
        azure_openai_api_version = "2023-05-15"
        if new_input is None: # return init message 
            return self.init_history[1]["content"]
        messages = self.init_history.copy()
        if history is not None:
            for user_question, bot_response in history:
                messages.append({"role":"user", "parts":user_question})
                messages.append({"role":"model", "parts":bot_response})
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=messages)
        response = chat.send_message(new_input)
        if not stream:
            return response.text
        else:
            return gpt_stream_wrapper(response)
    def run(self, **kwargs):
        return self.generate_response(**kwargs)
    

def check_args(function, args):
    sig = inspect.signature(function)
    params = sig.parameters

    # Check if there are extra arguments
    for name in args:
        if name not in params:
            return False
    # Check if the required arguments are provided 
    for name, param in params.items():
        if param.default is param.empty and name not in args:
            return False

    return True


class Smart_Agent(Agent):
    """
    Agent that can use other agents and tools to answer questions.

    Args:
        persona (str): The persona of the agent.
        tools (list): A list of {"tool_name":tool} that the agent can use to answer questions. Tool must have a run method that takes a question and returns an answer.
        stop (list): A list of strings that the agent will use to stop the conversation.
        init_message (str): The initial message of the agent. Defaults to None.
        engine (str): The name of the GPT engine to use. Defaults to "gpt-35-turbo".

    Methods:
        llm(new_input, stop, history=None, stream=False): Generates a response to the input using the LLM model.
        _run(new_input, stop, history=None, stream=False): Runs the agent and generates a response to the input.
        run(new_input, history=None, stream=False): Runs the agent and generates a response to the input.

    Attributes:
        persona (str): The persona of the agent.
        tools (list): A list of {"tool_name":tool} that the agent can use to answer questions. Tool must have a run method that takes a question and returns an answer.
        stop (list): A list of strings that the agent will use to stop the conversation.
        init_message (str): The initial message of the agent.
        engine (str): The name of the GPT engine to use.
    """

    def __init__(self, persona, functions_list, name=None, init_message=None, engine = 'gemini-pro' ):
        super().__init__(engine=engine,persona=persona, init_message=init_message, name=name)
       
        self.functions_list= functions_list
        
    
    def run(self, user_input, conversation=None, stream = False, api_version = "2023-07-01-preview"):
        model = genai.GenerativeModel('gemini-pro',tools=[CombinedTool])
        chat = model.start_chat(history = conversation)
        response =chat.send_message(user_input)

        while True:

                # Step 2: check if GPT wanted to call a function
            if  response.candidates[0].content.parts[0].function_call:
                print("Recommended Function call:")
                print( response.candidates[0].content.parts[0].function_call.name)
                print()
                
                # Step 3: call the function
                # Note: the JSON response may not always be valid; be sure to handle errors
                
                function_name =response.candidates[0].content.parts[0].function_call.name
                # verify function exists
                if function_name not in self.functions_list:
                    raise Exception("Function " + function_name + " does not exist")
                   
                function_to_call = self.functions_list[function_name]  
                
                # verify function has correct number of arguments
                function_args = dict(response.candidates[0].content.parts[0].function_call.args)
                print(function_args)

                if check_args(function_to_call, function_args) is False:
                    raise Exception("Invalid number of arguments for function: " + function_name)
                #search_query = function_args["search_query"]
                #print("search_query", search_query)

          

                function_response = function_to_call(**function_args)
                print("function")
                print(function_response)
                print()

                
                # Step 4: send the info on the function call and function response to GPT
                
                # adding assistant response to messages
                response = chat.send_message(
                        glm.Content(
                                        parts=[glm.Part(
                                        function_response = glm.FunctionResponse(
                                        name=function_name,
                                        response={'result': function_response}
                                                                      )
                                                                      )]
                                                                         )
                                                                            )

                # adding function response to messages
                # extend conversation with function response

                continue
            else:
                break #if no function call break out of loop as this indicates that the agent finished the research and is ready to respond to the user

        if not stream:
            assistant_response = response.text

        else:
            assistant_response = response.text

        return stream, conversation, assistant_response