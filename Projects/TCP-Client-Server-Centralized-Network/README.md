# TCP Centralized Client-Server Network 

Please use this README file to provide the following documentation for this project:

* Your name and student id
* General description of the project (a few sentences)
* If you used external Python modules/libraries. Provide a requeriments.txt file  
* Python version and compatibility issues (if any). Your project must be run exactelly as in the running instructions described below in this file
* Attach screenshots or videos to this file to ilustrate how your program works for all the options in the menu. 
* A few sentences about all the challenges you found during the implementation of this project and how you overcame them. Please be honest here. 

## Note that failure to provide the above docs will result in a 30% deduction in your final grade for this project. 

## Project Description and Detailed Guidelines (must read)

Detailed guidelines about this project can be found in this file. Failure to follow them may result in a bad grade in your project. Take this into consideration. Please read them carefully, and don't hesitate to ask the instructor for clarification if needed. 

The project goal is to create a basic server-client architecture network to provide basic functionalites/services to multiple clients. and explained in detail below.  
 
The project template provided in this repository is a good starting point, and will save you a lot of time in the implementation of this project. There are some methods that are already implemented by the class instructor in the template. For those methods that are not implemented, they provide starting point instruction about how to implement them. Note: if you decide to use this template, implement code for the parts marked as TODO.

You are not allowed to use any external python module/library other than the ones provided in the template. If I found out that you used additional libraries to complete the project without the instructor approval, you'll get a zero directly in the project.

You can implement this project either in both python 2 or 3 versions. However, you need to specify in the docs of this file which version you implemented. I will use this info to run your project with the appropiate commands.

## Project Template. 

This project template consist in five classes that are described in detail below: 

### Server 

The server class implements a TCP server socket after executed is put in listening mode waiting for other clients to connect. It must support multiple request at the same time (multiple threaded clients), and needs to take care of race conditions when to avoid write-write conflicts. The server class provides functionalities such as listen for clients, accept new clients, send data using client socket, and receive data from other clients. 

Once a client socket is connected to the server, the server accepts this client socket creating child process of it, and pass it as a parameter to a ClientHandler obkect. The ClientHandler object handles all the hard work done by the server when it needs to process data. 

The following is an example of console output after running the server. 

```
// server.py script executed in terminal
$ python server.py
Server listening at 127.0.0.1/12005
```
### ClientHandler

The client handler class is located in thee machine that is running the server. It is in charge of processing all the requests sent by clients, that needs to be processed by the server. It uses the server methods to send responses.  

### Client

The client class implements a TCP client socket that connects to a server socket running in a well know ip adress and port. The client class is in charge of interacting with the user, recopilate the user data, and send it to the server in a request to be processed. 

The following is an example of console output after running the client until the point that it shows the menu to the user. 

```
// client.py running in UNIX terminal
$ python Client.py
Enter the server IP Address: 127.0.0.1
Enter the server port: 12000
Your id key (i.e your name): Nina
Successfully connected to server with IP: 127.0.0.1 and port: 12000
Your client info is:
Client Name: Nina
Client ID: 50851

****** TCP Message App ******
-----------------------
Options Available:
1. Get user list
2. Sent a message
3. Get my messages
4. Create a new chat room
5. Join an existing chat room
6. Disconnect from server

Your option <enter a number>:
```

In the above example, the client connects to a server listening at 127.0.0.1/12000. Once the server accepts this client, the server assign and send a client id to this client. Once the server acknowledges that the client received the client id assigned to it, the handshake process is done. Finally, the client request the menu from the server, the server sends it, and the client shows the menu to the user waiting for the user input. 

### Menu: 

The menu class needs to be located on server side. The logic behind this is that a client does not know the services provided by the server until the client connects to the server. A real example of this is when a user requests a web page. The user, in this case, does not know anything about how this web site will look like until it inspects the response. In the same way, our client does not know anything about the menu until the server sends it in the response after the handshake. 

Once a client connects to the server, and the server sends the menu object with all their functionalities to the client, the client can use the menu to interact with the users. Note that only client and users can interact via the user menu. Server and client handler are only in charge of inspecting and processing requests from clients, and send their responses back to to the client.

The following is a detailed description of all the services/options that user menu must provide in this project. 

### Menu Options With Examples: 

* Option 1. Get User List 
   
When users select this option the client sends a request to the server asking for a list of all the users connected to    it. The server sends that list, and the users are show in console
  
```
Your option <enter a number>: 1
Users in server: Jose:2345, Nina:8763, Alice:1234, John:4566
```
The user format is <username:client_id>
  
* Option 2. Sent a message

When this option is selected, the client sends a request containing the option selected, the message entered by the user, and the recipient id. Once the server receives this requests, it iterates over a list containing all the clients handler objects to match the recipent_id of the message. Finally, the server saves the message in the appropiate handler, and acknowledges the client that the message was succesfully saved. 

The following is an example of the output provided by this option on the client side. 

```
Your option <enter a number>: 2
Enter your message: Hello World!
Enter recipent id: 50922
Message sent!
```
* Optiom 3. Get my messages

In this option, a user can requests to the server all the unread messages that are pending. This option is easy to implement because all the active client handler objects contain a list of the pending messages to be readed by the owner (clientsocket) of this object. 

The following is the output example, on client side, for this option.

```
Your option <enter a number>: 3
My messages:
2019-08-05 17:45: Hello World! (from: Nina)
2019-08-05 17:50: Are you there Jose? (from: Nina)
2019-08-05 17:52: This is Bob. What are you doing? (from: Bob)
```

* Optiom 4. Create a new chat room

A user selecting option 4 will create a new chat room for other users to join. It will ask to the user to enter the new chat room id, and sends the request to the server. Once the server acknowledges the request, the client keeps waiting for other members to join the chat. (option 5). Only the owner of the room can close it by entering 'exit'. Once the chat room is closed, the client console will show the user menu again. 

```
Your option <enter a number>: 4

Enter new room id: 3456
Your option <enter a number>: 4
Enter new chat room id: 23456

----------------------- Chat Room 23456 ------------------------ 

Type 'exit' to close the chat room.
Chat room created by: Jose
Waiting for other users to join....
```

* Optiom 5. Join an existing chat room

A user selecting option 5 will request to the server to be joined into an existing chat room. The user will enter the chat room id that wants to join, it will be sent to the server, the server will register the user into the corresponding chat room, and will acknowledge the client. Once the client is acknowledged, this user can chat with all the users registered in that chat room. Note that once users enter a chat room, they must see all the messages sent after they joined in their own console. Like in a real message app. Users (that are not owners of that chat room) can leave the chat by entering 'bye'. Once a user leaves a chat room, the console, on client side, must show the user menu again.

Below is an example of the joining process. 

```
Your option <enter a number>: 5

Enter chat room id to join: 3456

----------------------- Chat Room 23456 ------------------------
Joined to chat room 3456  
Type 'bye' to exit this chat room.
Alice joined
John joined.
Alice> Hello
Jose> Hello Alice, who is the moderator of this chat?
Bob> Hello Alice, and John. I am. How can I help you?
Alice> See you later. bye
Alice disconnected from the chat.
John> It looks like Alice was in a hurry.
Jose> agree. 
John> I am leaving too. Take care Bob. Bye.

****** TCP Message App ******
-----------------------
Options Available:
1. Get user list
2. Sent a message
3. Get my messages
4. Create a new chat room
5. Join an existing chat room
6. Disconnect from server

Your option <enter a number>:

```

* Option 6. Disconnect from server

A user selecting this option will requests to be disconnected from the server. The client sends the request to the server, then the server performs a cleanup of all the data related to that client in the server, and finally close the connection with that client socket. In addition, you also have the option to disconnect the client on the client side. Although this may work just fine, it is more prone to errors since the server still needs to do the cleanup of data for that socket (which do not exist anymore). 

## Running the project, 

You must follow exactelly this instructions in order to run and test your project. If I cannot run your project, as the following guidelines state, you'll get a zero in this project no matter how much work have you put on it. So, test it properly before final submission. 

This project consist in two main entities, the server and the client. Server and client must be run in different machines located in the same LAN. (Local Area Network). There are other additional classes that must be in the following machines. 

The files client_handler.py, and menu.py must be located in the same directory as the server.py file. The file client_helper.py must be located in the same directory as the client.py file. 

Additionally, This program must be compatible with the following OS architectures: Linux, Windows and macOS


Open a terminal in machine X and navigate to the directory where server.py is located. Then execute the following commands:

```
python server.py # if python 2 version 
python3 server.py # if python 3 version 
```
Take note of the server ip address in the LAN, so you can connect your clients to the server. 

Open a terminal in machine Y and navigate to the directory where client.py is located. Then execute the following commands:

```
python client.py # if python 2 version 
python3 client.py # if python 3 version 
```
## Project Submission

The due date of this project will be announced on ilearn, in class and by email. Projects are due before class, and it will be considered submitted only and only when students sent an email to the instructor <jortizco@sfsu.edu> with the link to your project in your repository using in the following email format. You can use it as a templete for your email. 
```
To: <jortizco@sfsu.edu>
Subject: CSC645-01 Computer Network: Client-Server Network Project Submission 
Body message:

Hi Professor Ortiz, 

My Client-Server Network Project has been completed. Here is the link to the project:

link: <your link>

<your name>
<your student id>
<your github username>

```

Good luck!!!











