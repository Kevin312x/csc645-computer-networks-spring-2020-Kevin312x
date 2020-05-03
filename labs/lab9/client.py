########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab4: TCP Client Socket
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Kevin Huynh
# Student ID: 916307020
# Student Github Username: kevin312x
# Instructions: Read each problem carefully, and implement them correctly. Your grade in labs is based on passing
#               all the unit tests provided.
#               The following is an example of output for a program that pass all the unit tests.
#               Ran 3 tests in 0.000s
#               OK
#               No partial credit will be given. Labs are done in class and must be submitted by 9:45 pm on iLearn.
########################################################################################################################
# don't modify this imports.
import pickle
import socket

######################################## Client Socket ###############################################################3
"""
1. Create a client class that implements a client socket. Implement methods send, receive, and close. 
2. Use your client class to connect to a server run by the instructor the ip address and port of the server
   will be provided by your instructor in class. 

"""


class Client(object):

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id = None
        self.student_name = "Kevin Huynh"  # TODO: your name
        self.github_username = "kevin312x"  # TODO: your username
        self.sid = 916307020
        self.server_ip = None

    def connect_to_server(self, server_ip_address, server_port):
        """
        Conne
        :param server_ip_address:
        :param server_port:
        :return:
        """
        self.client.connect((server_ip_address, server_port))
        data = self.receive()  # {'clientid': client_id, 'server_ip': server_ip}
        client_id = data['clientid']
        server_ip = data['server_ip']
        self.server_ip = server_ip
        self.client_id = client_id
        print("Client id " + str(self.client_id) + " connected to peer " + str(self.server_ip))
        while True:
            try:
                data = self.receive()
                if not data:
                    break
                print(data)
            except Exception as error:
                print(error)
        self.close()

    def send(self, data):
        data = pickle.dumps(data)
        self.client.send(data)

    def receive(self, max_buffer_size=4090):
        raw_data = self.client.recv(max_buffer_size)
        return pickle.loads(raw_data)

    def bind(self, ip, port):
        print(ip, port)
        self.client.bind((ip, port))

    def close(self):
        self.client.close()
