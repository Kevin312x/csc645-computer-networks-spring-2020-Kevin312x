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
import threading
import hashlib
######################################## Client Socket ###############################################################3
"""
1. Create a client class that implements a client socket. Implement methods send, receive, and close. 
2. Use your client class to connect to a server run by the instructor the ip address and port of the server
   will be provided by your instructor in class. 

"""


class Client(object):

    def __init__(self, peer):
        self.peer = peer
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
        # Connects to the server
        self.client.connect((server_ip_address, server_port))
        # Sends and receives a handshake
        data = self.peer.PWP.handshake(self.peer.INFO_HASH, self.peer.ID)
        self.send(data)
        data = self.receive()
        if data['info_hash'] != self.peer.INFO_HASH:
            print('Info Hash doesn\'t match')
            self.close()
        self.server_peer_id = data['peer_id']
        # data = self.receive()
        # self.peer.tracker.PEERS = data['tracker']
        # Receives the bitfield of the server and iterates through the
        # bitfield to determine if it contains a piece that the client is missing
        data = self.receive(8192)
        self.isMissing = False
        self.bitfield = self.peer.PWP._message(None, 5)
        self.peer_bitfield = data['bitfield']
        for i in range(len(self.peer_bitfield) - 1):
            for j in range(len(self.peer_bitfield[i]) - 1):
                if self.bitfield['bitfield'][i][j] != self.peer_bitfield[i][j]:
                    if self.bitfield['bitfield'][i][j] == 0:
                        self.isMissing = True
                        break
        # If client is interested in download, sends an interested request.
        if self.isMissing:
            data = self.peer.PWP._message(None, 2)
            self.send(data)
        else:
            data = self.peer.PWP._message(None, 3)
            self.send(data)
            self.close()
            return
        
        # Requests the server for blocks and stores it in tmp.txt file.
        while self.get_request():
            try:
                data = self.receive(8192)
                if not data:
                    self.close()
                    return
                if data['id'] == -1:
                    lock = threading.Lock()
                    lock.acquire()
                    with open('metainfo/tmp.txt', 'a') as age_file:
                        age_file.write(data['data'].decode('utf-8'))
                        self.peer.PWP.msg.set_block_to_completed(data['piece'], data['block'])
                        self.bitfield = self.peer.PWP._message(None, 5)
                        self.peer.routing(data['piece'], self.peer.swarm_id, self.server_peer_id, data['block'])
                    lock.release()

                    # After recieving a block, check the routing table to see if all the blocks of the piece
                    # is downloaded
                    blocks = 0
                    for obj in self.peer.ROUTING_TABLE:
                        if obj['piece_id'] == data['piece'] and obj['swarm_id'] == self.peer.swarm_id:
                            blocks += 1
                    
                    # If all the blocks of the piece is downloaded, extracts from the tmp file and sha1 a copy of it
                    # If the sha1 copy matches the .torrent file, successfully downloaded the piece.
                    if blocks == 8:
                        piece = ''
                        block = 0
                        for obj in self.peer.ROUTING_TABLE:
                            if obj['piece_id'] == data['piece'] and obj['swarm_id'] == self.peer.swarm_id and obj['block_id'] == block:
                               with open('metainfo/tmp.txt', 'r') as age_file:
                                   age_file.seek(self.peer.block_length * obj['index'])
                                   piece += age_file.read(self.peer.block_length)
                                   block += 1
                        # self.peer.routing_del(data['piece'], self.peer.swarm_id)
                        piece_copy = piece.encode('utf-8')
                        sha1 = hashlib.sha1()
                        sha1.update(piece_copy)
                        hash = sha1.digest()
                        if self.peer.compare_hash(hash, data['piece']) == 1:
                            print('match')
                            # payload = {'piece_index': data['piece']}
                            # data = self.peer.PWP._message(payload, 4)
                            # self.send(data)
                        else:
                            print('corrupted')

                elif data['id'] == 0:
                    while True:
                        data = self.receive()
                        if data['id'] == 1:
                            break
                elif data['id'] == 4:
                    piece = data['piece_index']
                    self.peer_bitfield[piece].setall(1)
                elif data['id'] == 'tracker':
                    self.peer.tracker.PEERS = data['tracker']
            except Exception as error:
                print(error)
                self.close()

    # Iterates over the server's bitfield and compares with yours.
    # If missing any, sends a request to the server for the block.
    def get_request(self):
        for i in range(len(self.peer_bitfield)):
            for j in range(len(self.peer_bitfield[i])):
                if self.bitfield['bitfield'][i][j] != self.peer_bitfield[i][j] and self.bitfield['bitfield'][i][j] == 0:
                    payload = {'index': i, 'begin': self.peer.piece_length * i, 'block': self.peer.block_length * j}
                    data = self.peer.PWP._message(payload, 6)
                    self.send(data)
                    return 1
        return -1

    def send(self, data):
        data = pickle.dumps(data)
        self.client.send(data)

    def receive(self, max_buffer_size=4090):
        raw_data = self.client.recv(max_buffer_size)
        return pickle.loads(raw_data)

    def bind(self, ip, port):
        self.client.bind((ip, port))

    def close(self):
        self.client.close()
