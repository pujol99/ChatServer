# ChatServer

Program that creates a chat server within a domestic connection

# Habilities

- send messages to everybody in the chat room
- send messages to a specific person in the chat
- see who is in the chat
- put your name for being recognized

# Prerequisits

- python version 3 or newer

guide to install python: https://www.youtube.com/watch?v=OV9WlTd9a2U

# Load the program

First use the console to navigate to the folder where the scripts are, then you have to create the server executing the program > `python server.py` or `python3 server.py` depending on your version, then you have to check the IP of the server/computer, to connect to that IP, when you know the IP change the variable SERVER_IP in `client.py`, then execute the program from any computer console in the network and execute > `python client.py` or `python3 client.py` depending on your version, you can connect as many computers as you desire

# How it works

With the socket and threading library u can send and recieve messages, the messages are sent to the server by the threads/computers and then the server sends back the message to all the threads.

Before sending the message the thread will ZIP the message with other important information like who will recieve it, who send it, some special tags... and when the other threads recieve the message they will UNZIP the message to understand what to do

![s2](https://user-images.githubusercontent.com/33929967/65261710-1f6df800-db09-11e9-807c-47f48dce5398.png)


