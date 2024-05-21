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

template_messages = [
    SystemMessage(content='''
                  You interpret commands to pass to a robot. It is important that your output is in the form of a JSON dictionary. 
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
                  
                  As an example, if the user asks you to drive to a cola can, your response shoud be:
                  dict = {
                    "function": drive_to,
                    "color": 'red'
                  }
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


while True:
    print('Ask me anything: ', end='')
    question = input()
    print(runnable.invoke(question))
