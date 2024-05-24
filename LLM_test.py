from lib.LLM import LLM

if __name__ == '__main__':
    llm = LLM()

    while True:
      print('Ask me anything: ', end='')
      question = input()
      with open('picarx/temp/question.txt', 'w') as file:
         file.write(question)

      LLM.answer('picarx/temp/question.txt','picarx/temp/answer.txt')
      with open('picarx/temp/answer.txt', 'r') as file:
         text = file.read()
      print(text)
