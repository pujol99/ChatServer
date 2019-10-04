# ChatServer

Program that creates a chat server within a domestic connection

# Habilities

- send messages to everybody in the chat room
- send messages to a specific person in the chat
- see who is in the chat
- put your name for being recognized

# Prerequisits

First you have to create the server executing the program > `python chat.py` or `python3 chat.py` depending on your version, then you have to check the IP of the server to connect to that IP, when you now the IP you can execute the program from the computer you want in the network and execute > `python chat.py server-ip` or `python3 chat.py server-ip` depending on your version (change server-ip for the actual server ip!), you can connect many computers as you want

# Load the program

First use the console to navigate to the folder where the script is, then you have to create the server executing the program > `python chat.py` or `python3 chat.py` depending on your version, then you have to check the IP of the server to connect to that IP, when you now the IP you can execute the program from any computer console in the network and execute > `python chat.py server-ip` or `python3 chat.py server-ip` depending on your version (replace `server-ip` for the actual server ip!), you can connect as many computers as you desire

# How it works

With the socket and threading library u can send and recieve messages, the messages are sent to the server by the threads and then the server sends back the message to all the threads.

Before sending the message the thread will zipped with other import information like who will recieve it, who send it, some special tags... and when the other threads recieve the message they will unzip the message to understand what to do

![s2](https://user-images.githubusercontent.com/33929967/65261710-1f6df800-db09-11e9-807c-47f48dce5398.png)


