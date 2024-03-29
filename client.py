import socket
import threading
import sys
import datetime

""" CHANGE IT TO YOUR'S"""
SERVER_IP = '192.168.0.18'
"""####################"""


class Client:		
	def __init__(self):
		#CONNECT TO SERVER
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((SERVER_IP, 10000))
		
		#VARIABLES
		self.message = ''
		self.name = ''
		self.myIp = self.sock.getsockname()[0]
		
		#CHAT INFO
		self.display_menu()
		
		#MAIN LOOP
		self.loop()
	
	def display_menu(self):
		print('\nWelcome to the chat room!\n')
		print('Comands:')
		print('  Set your name           !name your_name')
		print('  Send private message    !to ip/name msg')
		print('  See who is connected    !people')
		print('  Clean chat              !clear')
		print('  Log out                 !exit')
	
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
			
		elif '!clear' in self.message:
			print('\n\n\n\n\n\n\n\n')
			print('\n\n\n\n\n\n\n\n')
			print('\n\n\n\n\n\n\n\n')
			self.display_menu()
			self.sock.send(bytes(self.zip('', '', 'clear'), 'utf-8'))
		else:
			#WE SEND A NORMAL MESSAGE TO ALL THREADS
			self.sock.send(bytes(self.zip('', self.message), 'utf-8'))
	
	def zip(self, to, msg, tag=None):
		#WE WILL ZIP ALL MESSAGE INFORMATION INTO A PACKET
		now = datetime.datetime.now()
		packet = ''
		
		packet += 'name:'
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
		packet += ',time:'		#we will include the hour of sending
		packet += self.beauty(now.hour) + ':' + self.beauty(now.minute)
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
		time = data[5][5:]
		
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
		elif 'clear' in tag:
			#RECIEVER DOES NOTHING
			return ''
		else:
			#IF ITS A NORMAL MESSAGE WE SIMPLY BUILD IT WITH SENDER NAME AND MESSAGE
			if ip_recv not in 'all':			#if the message is not for us we dont print it
				if self.myIp not in ip_recv:
					if self.name != ip_recv:
						return

			if self.myIp in ip_send:			#if we send it we'll put us as sender
				packet = '<You ' + time + '> '
			else:								#if was another person we'll put his name or ip
				if name is not '':
					packet = '<' + name + ' ' + time + '> '
				else:
					packet = '<' + ip_send + ' ' + time + '> '
			packet += msg						#we add the message
			return packet
	
	def beauty(self, num):
		if num < 10:
			return '0' + str(num)
		else:
			return str(num)


def main():
	client = Client()

if __name__ == "__main__":
	main()