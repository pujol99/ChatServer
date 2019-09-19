import socket
import threading
import sys

class Client:		
	def __init__(self, adress):
		#CONNECT TO SERVER
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((adress, 10000))
		
		#VARIABLES
		self.message = ''
		self.name = ''
		self.myIp = self.sock.getsockname()[0]
		
		#CHAT INFO
		print('\nWelcome to the chat room!\n')
		print('Comands:')
		print('  Set your name           !name your_name')
		print('  Send private message    !to ip/name msg')
		print('  See who is connected    !people')
		print('  Log out                 !exit')
		
		#MAIN LOOP
		self.loop()
	
	def loop(self):
		while True:
			#SENDING PART
			iThread = threading.Thread(target=self.sendMsg)
			iThread.daemon = True
			iThread.start()
			
			#RECIEVING PART
			data = self.sock.recv(1024)
			if not data:
				print('Server offline')
				break
			self.recvMsg(data)
			
	def sendMsg(self):
		self.message = input("")
		
		#LOOK FOR COMANDS
		if '!exit' in self.message:
			#CLOSE THREAD
			self.sock.shutdown(socket.SHUT_RDWR)
			self.sock.close()
			return
			
		elif '!name' in self.message:
			#CHANGE OUR NAME AND NOTIFY OTHERS
			self.name = self.message[6:]
			info = ' (' + self.myIp + ' set his name to ' + self.name + ')'
			self.sock.send(bytes(self.zip('', info), 'utf-8'))
			
		elif '!to' in self.message:
			#ONLY ONE IP WILL RECIEVE MESSAGE
			info = self.message.split()
			to = info[1]
			msg = ' '.join(info[2:])
			self.sock.send(bytes(self.zip(to, msg), 'utf-8'))
			
		elif '!people' in self.message:
			#WE WILL ASK EVERYBODY TO TELL US THEIR NAME ADDING A SPECIAL TAG 'NAMES'
			print('People in the chat:')
			self.askingForNames = True
			self.sock.send(bytes(self.zip('', '', 'names'), 'utf-8'))
			
		else:
			#WE SEND A NORMAL MESSAGE TO ALL THREADS
			self.sock.send(bytes(self.zip('', self.message), 'utf-8'))
	
	def zip(self, to, msg, tag=None):
		#WE WILL ZIP ALL MESSAGE INFORMATION INTO A PACKET
		packet = 'name:'
		if self.name:
			packet += self.name
		packet += ',msg:' 		#the message
		packet += msg
		packet += ',ip:'		#our ip so they know who send it
		packet += self.myIp
		packet += ',to:'		#we will decide who recv message all or one
		if to:
			packet += to
		else:
			packet += 'all'
		packet += ',tag:'		#we can include a tag for special functions
		if tag:
			packet += tag
		return packet
		
	def recvMsg(self, data):
		data = str(data, 'utf-8')
		
		data = self.unzip(data)
		if data:
			print(data)
	
	def unzip(self, data):
		#WE WILL UNZIP THE MESSAGE TO KNOW WHAT TO DO
		data = data.split(',')
		name = data[0][5:]
		msg = data[1][4:]
		ip_send = data[2][3:]
		ip_recv = data[3][3:]
		tag = data[4][4:]
		
		if 'names' in tag:
			#THIS TAG MEANS WE HAVE BEEN REQUIRED OUR NAME OR IP, SO WE SEND IT TO WHO HAS DONE THE REQUEST
			if self.name:
				self.sock.send(bytes(self.zip(ip_send, self.name, 'myName'), 'utf-8'))
			else:
				self.sock.send(bytes(self.zip(ip_send, self.myIp, 'myName'), 'utf-8'))
		elif 'myName' in tag:
			#THIS TAG MEANS WE ARE RECIEVING A NAME INFO IF WE ARE THE PERSON WHO ASKED WE PRINT INFO
			if self.myIp in ip_recv:
						print('\t', msg)
		else:
			#IF ITS A NORMAL MESSAGE WE SIMPLY BUILD IT WITH SENDER NAME AND MESSAGE
			if ip_recv not in 'all':			#if the message is not for us we dont print it
				if self.myIp not in ip_recv:
					if self.name != ip_recv:
						return

			if self.myIp in ip_send:			#if we send it we'll put us as sender
				packet = '<You> '
			else:								#if was another person we'll put his name or ip
				if name is not '':
					packet = '<' + name + '> '
				else:
					packet = '<' + ip_send + '> '
			packet += msg						#we add the message
			return packet
	

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
	if (len(sys.argv) > 1):
		client = Client(sys.argv[1])
	else:		
		server = Server()
		server.run()
	

if __name__ == "__main__":
	main()