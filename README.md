# ChatServer

Program that creates a chat server within a domestic connection

# Habilities

- send messages to everybody in the chat room
- send messages to a specific person in the chat
- see who is in the chat
- put your name for being recognized

# Load the program

First you have to create the server executing the program > `python chat.py` then you have to check the IP of the server to connect to that IP, when you now the IP you can execute the program from the computer you want in the network and execute > `python chat.py server-ip` you can connect many computers as you want

# How it works

With the socket and threading library u can send and recieve messages, the messages are sent to the server by the threads and then the server sends back the message to all the threads.

Before sending the message the thread will zipped with other import information like who will recieve it, who send it, some special tags... and when the other threads recieve the message they will unzip the message to understand what to do

![s2](https://user-images.githubusercontent.com/33929967/65261586-e6ce1e80-db08-11e9-92da-91b30b0ae600.png)

