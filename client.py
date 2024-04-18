import socket
from threading import Thread
import random

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = "127.0.0.1"
port = 8000

client.connect((ip_address, port))

print("Connected to the server!")

nickname = input("Nickname: ")

def receive():
	while True:
		try:
			message = client.recv(2048).decode("utf-8")
			if message == "NICKNAME":
				client.send(nickname.encode("utf-8"))
			else:
				print("Message received: ",message)
		except:
			print("An error occured!")
			client.close()
			break

def write():
	while True:
		message = client.recv(2048).decode("utf-8")
		try:
			if message == "Please enter your answer: ":
				answer = input("Your answer (A/B/C/D): ")
				client.send(answer.encode("utf-8"))
			else:
				print("Message received: ",message)
		except:
			print("An error occured!")
			client.close()
			break

#initiating and starting the threads
receive_thread = Thread(target=receive)
receive_thread.start()

write_thread = Thread(target=write)
write_thread.start()