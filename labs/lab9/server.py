########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: TCP Server Socket
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

######################################### Server Socket ################################################################
"""
Create a tcp server socket class that represents all the services provided by a server socket such as listen and accept
clients, and send/receive data. The signatures method are provided for you to be implemented
"""
import pickle
import socket
from threading import Thread


# import urllib.request


class Server(object):

    def __init__(self, ip_address='127.0.0.1', port=5000):
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        self.ip = ip_address
        self.port = port
        self.serversocket.bind((ip_address, port))

    def _listen(self):
        """
        Private method that puts the server in listening mode
        If successful, prints the string "Listening at <ip>/<port>"
        i.e "Listening at 127.0.0.1/10000"
        :return: VOID
        """
        try:
            self.serversocket.listen(5)
            # uncomment the line below to router point of entry ip address
            # self.ip = urllib.request.urlopen('http://ifconfig.me/ip').read() 
            print("Listening for new peers at " + str(self.ip) + "/" + str(self.port))

        except Exception as error:
            print(error)

    def _accept_clients(self):
        """
        Accept new clients
        :return: VOID
        """
        while True:
            try:
                # accept connections from outside
                (clientsocket, address) = self.serversocket.accept()
                # now do something with the clientsocket
                # in this case, we'll pretend this is a threaded server
                Thread(target=self.client_thread, args=(clientsocket, address)).start()
                print("Client: " + str(address[1]) + " just connected")
            except Exception as error:
                print(error)

    # noinspection PyMethodMayBeStatic
    def append_to_file(self, data, file="connFile.txt"):
        f = open(file, "a+")
        f.write(data)
        f.write('\n')
        f.close()

    # noinspection PyMethodMayBeStatic
    def _send(self, client_socket, data):
        """
        :param client_socket:
        :param data:
        :return:
        """
        data = pickle.dumps(data)
        client_socket.send(data)

    # noinspection PyMethodMayBeStatic
    def _receive(self, client_socket, max_buffer_size=4096):
        raw_data = client_socket.recv(max_buffer_size)
        return pickle.loads(raw_data)

    def client_thread(self, clientsocket, address):
        """
        Implement in lab4
        :param clientsocket:
        :param address:
        :return:
        """

        server_ip = str(address[0] + "/" + str(self.port))
        client_id = address[1]
        data = {'clientid': client_id, 'server_ip': server_ip}
        self._send(clientsocket, data)

    def run(self):
        self._listen()
        self._accept_clients()
