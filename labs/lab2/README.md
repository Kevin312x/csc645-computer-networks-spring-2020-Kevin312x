# Lab #2: TCP Client Socket 
Please read this README file before class and use this as a reference during the lab session. 

In this lab, students will learn how to create a TCP client socket. Please read the instructions provided in this lab 
carefully. The file provided in this lab has been partially implemented by your instructor. Your job in this lab is to implement only the parts marked as TODO. 

## Useful hints to follow in this lab 

### How to create a client socket. 

1. In order to create a client socket, first you need to import the socket library builtin in the standad Python libraries.
The socket library provides all the low level functions needed.
2. The following line of code creates a client socket. So, you can use that socket to call 
methods such as connect(), send(), recv()...
```python
# TCP client socket
import socket
# AF_INET is the connection domain. In this case, IPv4
# SOCK_STREAM is the type of connection. STREAM means that that socket will use a TCP based connection
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
```  
3. Connect to a well know server. A well know server is a server which IP address, port or hostname is well know by the 
client. In this lab. you can assume that your client will connect to a server via Local Area Network (LAN), and the IP 
address and port of the server will be provided by the instructor. 
```python
# Connects to a server socket running at 127.0.0.1/12000
# In your lab, you need to provide error handling mechanisms
# to handle connection errors (i.e server is not running)
server_ip_address = "127.0.0.1"
server_port = 12000
clientsocket.connect((server_ip_address, server_port))
```
4. After the server accepts the connection, it will assign and send a unique client id to the client. This client id will
define the client in the network. (more about this in server side in next lab). The data (client id or any other data) 
sent by the server is serialized in a stream of bytes. Upon receiving this data, the client needs to deserialize it, so it can be processed properly. There are many ways to do the serialization and deserialization of the data, in this lab we use 
pickle library which makes our job a lot easier. 
```python
import pickle 
MAX_MEM_ALLOC = 4096
# stream of bytes from server. Note that recv(..) method is a blocking method. 
serialized_data = clientsocket.recv(MAX_MEM_ALLOC) 
# deserialized the data. Now is a python dictionary again {'cliientid:<assigned id>}
deserialized_data = pickle.loads(serialized_data)  
clientid = serialized_data['clientid']
print("Assigned client id by server: ", clientid)
```

5. Now that the handshake between client and server is completed, it is time for the client to send data to the server. In 
this example, our name and email is sent to the server. 
```python
name = "Jose Ortiz"
email = "jose@sfsu.edu"
# create the container (dict) to send the data 
data = {'name':name, 'email':email} 
# serializes the data. Data is ready to go.
serialized_data = pickle.dumps(data)  
# sends the serialized data to server. 
clientsocket.send(serialized_data)
```

6. How do we know if the server received the data that the client just sent?. The server acknowledges that the data was 
received. Note that no error in sending the data does not mean that the server received the data. 
(i,e server closed the connection before receiving the data). That is why you need to implement in your server (next lab)
a way to acknowledge to the client that the data was successfully received.  

Since in this lab you are not implementing the server socket, and do not know anything about the server acknowledges, you
can assume that the server received your data when you see proof of it in the projector screen showing the server 
console log. 

### How to keep the client alive waiting for server responses?

Take into consideration that a client needs to be listening all the time for server responses even if the client did not 
send a request. Otherwise, the client program would be terminated and therefore, its connection to the server would be automatically closed by the client program. How can we implement the client to be in listening mode all the time? Hint: try to put clientsocket.recv() in a forever loop, and only break it when there is no more data comming from the server. 

```python
# client keeps listening for more data
while True: 
   data = clientsocket.recv(MAX_MEM_ALLOC) # blocking method. 
   if not data: 
       break
   # process the data here.
```


## Testing you client socket

At the beginning of the lab, the instructor will run a TCP server program that accepts multiple clients. The console 
with the output of the program will be show to all the class in the class projector. The IP address and port of the 
server will be given to you in class. 

You'll get full grade in this lab only if your TCP client program successfully connects to the server running in the 
class projector. Once your client program connects to the server, the server console will show your name, student id, 
and github username in the class projector.
