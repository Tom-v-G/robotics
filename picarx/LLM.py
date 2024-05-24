from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

class LLM:
    template_messages = [
        SystemMessage(content='''
                    You are an assistant that interprets commands which are passed on to a robot. 
                    You give answers which consist of two parts: a short response in which you describe what task the robot is going to perform, and a 
                    JSON dictionary that will be given to the robot.It is important that the second part of your answer is a JSON dictionary with the name json_dict. 
                    The dictionary has the following form:
                    dict = {
                        "function": FUNCTION,
                        "color": COLOR
                    }
                    The FUNCTION keyword should be replaced with the function that the user wants you to use. 
                    When asked to drive to an object, FUNCTION should be 'drive_to'. When asked to grab an object, FUNCTION should be 'grab'.
                    COLOR should be the color of the object (as a string) that the user asks you to interact with. 
                    
                    Here is a list of objects and their color:
                        - cola can: red
                        - fanta can: orange
                        - cassis can: purple
                        - pepsi can: grey
                    
                    As an example, if the user asks you: "Drive to the cola can" your response should be:
                    "Certainly, I will drive to the cola can!
                    json_dict = {
                        "function": drive_to,
                        "color": 'red'
                    }"
                    '''),
        # MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]

    model = Ollama(model="llama3:latest")
    prompt_template = ChatPromptTemplate.from_messages(template_messages)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    #chain = LLMChain(llm=model, prompt=prompt_template, memory=memory)


    runnable = (
        {"text": RunnablePassthrough()} | prompt_template | model | StrOutputParser()
    )

    def answer(question_filepath, answer_filepath):

        with open(question_filepath, 'r') as file:
            text = question_filepath.read()
            text = ' '.join(text.rsplit(' ')[:-1]) # remove termination keyword
            answer = LLM.runnable.invoke(text)
            
        with open(answer_filepath, 'w') as file:
            file.write(answer)
        
