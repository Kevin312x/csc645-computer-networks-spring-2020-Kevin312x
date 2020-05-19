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
import bencode
from threading import Thread

import urllib.request


class Server(object):

    def __init__(self, ip_address='127.0.0.1', port=5000):
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        # Receives and sends a handshake
        data = self._receive(clientsocket)
        if data['info_hash'] != self.INFO_HASH:
            print('Info Hash doesn\'t match')
            return
        data = self.PWP.handshake(self.INFO_HASH, self.ID)
        self._send(clientsocket, data)
        # self.tracker.addPeer(address[0], address[1], clientsocket)
        # self.tracker.sendPeersIPAddress()
        # Sends the bitfield to the client.
        data = self.PWP._message(None, 5)
        self._send(clientsocket, data)
        while True:
            data = self._receive(clientsocket)
            if not data:
                break
            if data['id'] == 0:
                pass
            elif data['id'] == 1:
                pass
            elif data['id'] == 2:
                pass
            elif data['id'] == 3:
                pass
            elif data['id'] == 4:
                pass
            elif data['id'] == 5:
                pass
            elif data['id'] == 6:
                # Reads from age.txt file to get a specific block, then sends it to client.
                begin = data['begin']
                block = data['length']
                with open('metainfo/age.txt', 'r') as age_file:
                    age_file.seek(begin + block)
                    block_read = age_file.read(self.block_length).encode('utf-8')
                    data = {'id': -1, 'piece': data['index'], 'block': int(block / self.block_length), 'data': block_read}
                    self._send(clientsocket, data)
                
            elif data['id'] == 7:
                pass
            elif data['id'] == 8:
                pass
            elif data['id'] == 9:
                pass

    def run(self):
        self._listen()
        self._accept_clients()