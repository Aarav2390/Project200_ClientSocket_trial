import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address = "127.0.0.1"
port = 8000
server.bind((ip_address,port))
server.listen()

list_of_clients = []
nicknames = []

questions = [
    "What is the capital city of Australia? \nA. Melbourne \nB. Sydney \nC. Canberra \nD. Perth",
    "What is the largest organ in the human body? \nA. Skin \nB. Brain \nC. Liver \nD. Heart",
    "In which year did the Titanic sink? \nA. 1909 \nB. 1921 \nC. 1933 \nD. 1912",
    "What is the chemical symbol for gold? \nA. Pt \nB. Au \nC. Fe \nD. Ag",
    "Which planet is known as the 'Red Planet'? \nA. Saturn \nB. Jupiter \nC. Venus \nD. Mars",
    "Who painted the famous artwork 'Starry Night'? \nA. Leonardo da Vinci \nB. Vincent van Gogh \nC. Michelangelo \nD. Pablo Picasso",
    "What is the longest river in the world? \nA. Amazon \nB. Nile \nC. Yangtze \nD. Mississippi",
    "Who is the author of the Harry Potter book series? \nA. Stephenie Meyer \nB. George R.R. Martin \nC. J.K. Rowling \nD. J.R.R. Tolkien"
]

answers=["C", "A", "D", "B", "D", "B", "A", "C"]

def get_random_question_answer(conn):
  #generating random question and storing correct ans for it
  questNum = random.randint(0, len(questions)-1)
  question = questions[questNum]
  answerNum = questNum
  correct_answer = answers[answerNum]
  
  #asking question and receiving answer
  conn.send(question.encode("utf-8"))
  conn.send("Please enter your answer: ".encode("utf-8"))
  recvAnswer = (conn.recv(2048).decode("utf-8")).upper()
  
  return question,correct_answer,recvAnswer,questNum,answerNum

def remove_question(recv_ans, questNum, answerNum):
  questions.remove(questNum)
  answers.remove(answerNum)
  
def clientthread(conn):

  #score variable and instructions
  client_score = 0
  conn.send("Welcome to the quiz game!\n".encode("utf-8"))
  conn.send("You will be asked a series of question with answers A, B, C or D\n".encode("utf-8"))
  conn.send("Choose the correct answer for points!\n".encode("utf-8"))
  conn.send("Good luck!!\n\n".encode("utf-8"))


  #saving correct question, correct answer and received answer
  question, correct_answer, recvAnswer, questNum, answerNum = get_random_question_answer(conn)

  while True:
    #checking if message is valid
    if recvAnswer not in answers:
      list_of_clients.remove(conn)

    #checking if ans is correct and sending msg
    if recvAnswer == correct_answer:
      client_score += 1
      correct_message = "Correct answer ✅! Your score is now {}".format(client_score)
      conn.send(correct_message.encode("utf-8"))
      get_random_question_answer(conn)

    else:
      wrong_message = "Incorrect answer ❌! Your score is {}".format(client_score)
      conn.send(wrong_message.encode("utf-8"))
      remove_question(recvAnswer,questNum,answerNum)
      get_random_question_answer(conn)

while True:
  conn,adr = server.accept()
  list_of_clients.append(conn)
  nickname = conn.recv("NICKNAME".encode("utf-8"))
  nicknames.append(nickname)

  message = "{} has joined!".format(nickname)
  print(message)
  
  new_thread = Thread(target= clientthread, args=(conn,adr))
  new_thread.start()