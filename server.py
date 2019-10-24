import socket
import threading
import sys

class Server:
	def __init__(self):
		#SET UP SERVER
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(('0.0.0.0', 10000))
		self.sock.listen(1)
		
		self.connections = []
		
	def run(self):
		print('Chat room created!')
		while True:
			c, a = self.sock.accept()
			
			#CREATE INDEPENDENT THREAD 
			cThread = threading.Thread(target=self.handler, args=(c, a))
			cThread.daemon = True
			cThread.start()
			
			#APPEND IT AS NEW CONNECTION
			self.connections.append(c)
			print(str(a[0]), "joined chat")
	
	def handler(self, c, a):
		while True:
			#WAIT TO RECIEVE DATA
			data = c.recv(1024)
			data = str(data, 'utf-8')
			
			#IF THERE'S NO DATA WE LOST COMMUNICATION
			if not data:
				print(str(a[0]), "disconnected")
				self.connections.remove(c)
				c.close()
				break
			
			#SEND THE DATA RECIEVED TO ALL THREADS
			for connection in self.connections:
				connection.send(bytes(data, 'utf-8'))

def main():
	server = Server()
	server.run()
	

if __name__ == "__main__":
	main()