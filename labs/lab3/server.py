########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: TCP Server Socket
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Kevin Huynh
# Student ID: 916307020
# Student Github Username: kevin312x
# Lab Instructions: No partial credit will be given. Labs must be completed in class, and must be committed to your
#               personal repository by 9:45 pm.
# Program Running instructions:
#               Version Python 3.6.9
########################################################################################################################

# don't modify this imports.
import socket
import pickle
from threading import Thread

class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10 # keeps 10 clients in queue

    def __init__(self, host="127.0.0.1", port = 12000):
        """
        Class constructor
        :param host: by default localhost. Note that '0.0.0.0' takes LAN ip address.
        :param port: by default 12000
        """
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TODO: create the server socket

    def _bind(self):
        """
        # TODO: bind host and port to this server socket
        :return: VOID
        """
        self.serversocket.bind((self.host,self.port))
        self.serversocket.listen(self.MAX_NUM_CONN)

    def _listen(self):
        """
        # TODO: puts the server in listening mode.
        # TODO: if succesful, print the message "Server listening at ip/port"
        :return: VOID
        """
        try:
            self._bind()
            # your code here
            print("Server listening at " + self.host + '/' + str(self.port))
        except:
            self.serversocket.close()

    def _handler(self, clienthandler):
        """
        #TODO: receive, process, send response to the client using this handler.
        :param clienthandler:
        :return:
        """
        while True:
             # TODO: receive data from client
             self.recieve_data = self.receive(clienthandler)
             if not self.recieve_data:
                 break
             else:
                 print(self.recieve_data)
             # TODO: if no data, break the loop
             # TODO: Otherwise, send acknowledge to client. (i.e a message saying 'server got the data

    def _accept_clients(self):
        """
        #TODO: Handle client connections to the server
        :return: VOID
        """
        while True:
            try:
               clienthandler, addr = self.serversocket.accept()
               # TODO: from the addr variable, extract the client id assigned to the client
               # TODO: send assigned id to the new client. hint: call the send_clientid(..) method
               self._send_clientid(clienthandler, addr[1])
               self._handler(clienthandler) # receive, process, send response to client.
            except:
               # handle exceptions here
               raise  #remove this line after implemented.

    def _send_clientid(self, clienthandler, clientid):
        """
        # TODO: send the client id to a client that just connected to the server.
        :param clienthandler:
        :param clientid:
        :return: VOID
        """
        data = {'clientid': clientid}
        self.send(clienthandler, data)


    def send(self, clienthandler, data):
        """
        # TODO: Serialize the data with pickle.
        # TODO: call the send method from the clienthandler to send data
        :param clienthandler: the clienthandler created when connection was accepted
        :param data: raw data (not serialized yet)
        :return: VOID
        """
        self.serialezed_data = pickle.dumps(data)
        clienthandler.send(self.serialezed_data)

    def receive(self, clienthandler, MAX_ALLOC_MEM=4096):
        """
        # TODO: Deserialized the data from client
        :param MAX_ALLOC_MEM: default set to 4096
        :return: the deserialized data.
        """
        
        self.serialized_data = pickle.loads(clienthandler.recv(MAX_ALLOC_MEM))
        return self.serialized_data #change the return value after implemente.

    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """
        self._listen()
        self._accept_clients()

# main execution
if __name__ == '__main__':
    server = Server()
    server.run()











