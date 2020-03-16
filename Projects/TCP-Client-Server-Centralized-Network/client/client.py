#######################################################################
# File:             client.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template client class. You are free to modify this
#                   file to meet your own needs. Additionally, you are 
#                   free to drop this client class, and add yours instead. 
# Running:          Python 2: python client.py 
#                   Python 3: python3 client.py
#
########################################################################
import socket
import pickle
import sys
import os
sys.path.append(os.path.abspath('../server'))
import menu

class Client(object):
    """
    The client class provides the following functionality:
    1. Connects to a TCP server 
    2. Send serialized data to the server by requests
    3. Retrieves and deserialize data from a TCP server
    """

    def __init__(self):
        """
        Class constractpr
        """
        # Creates the client socket
        # AF_INET refers to the address family ipv4.
        # The SOCK_STREAM means connection oriented TCP protocol.
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientid = 0
        
    def get_client_id(self):
        data = self.receive()
        client_id = data['clientid']
        self.client_id = client_id
        print("Client id " + str(self.client_id) + " assigned by server")

    
    def connect(self, host="127.0.0.1", port=12000):
        """
        TODO: Connects to a server. Implements exception handler if connection is resetted. 
	    Then retrieves the cliend id assigned from server, and sets
        :param host: 
        :param port: 
        :return: VOID
        """
        self.host = input("Enter the server IP Address: ")
        self.port = input("Enter the server port: ")
        self.name = input("Your id key (i.e your name): ")
        self.clientSocket.connect((self.host, int(self.port)))
        self.get_client_id()

        name = {'client_name' : self.name}
        self.send(name)

        self.get_menu()
        self.menu.process_user_data()
        
        self.close()
	
    def send(self, data):
        """
        TODO: Serializes and then sends data to server
        :param data:
        :return:
        """
        data = pickle.dumps(data)
        self.clientSocket.send(data)

    def receive(self, MAX_BUFFER_SIZE=4090):
        """
        TODO: Desearializes the data received by the server
        :param MAX_BUFFER_SIZE: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        self.raw_data = self.clientSocket.recv(MAX_BUFFER_SIZE)
        return pickle.loads(self.raw_data)
        

    def close(self):
        """
        TODO: close the client socket
        :return: VOID
        """
        self.clientSocket.close()

	
    def get_menu(self):
        data = self.receive()
        menu = data['menu']
        self.menu = menu
        self.menu.set_client(self)


if __name__ == '__main__':
    client = Client()
    client.connect()
