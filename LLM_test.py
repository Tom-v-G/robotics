from lib.LLM import LLM

if __name__ == '__main__':
    llm = LLM()

    while True:
      print('Ask me anything: ', end='')
      question = input()
      with open('temp/question.txt', 'w') as file:
         file.write(question)

      llm.answer('temp/question.txt','temp/answer.txt')
      with open('temp/answer.txt', 'r') as file:
         text = file.read()
      print(text)
