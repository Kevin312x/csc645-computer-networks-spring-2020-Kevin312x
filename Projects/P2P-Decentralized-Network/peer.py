"""
Lab 9: Routing and Handing
Implement the routing and handling functions
"""

# CSC645 Computer Networks
# Lab 8 Solution: peer.py
# Author: Kevin Huynh
# client and server files are from lab 2. However, the server supports multi-threading like in lab 4

from server import Server
from threading import Thread
from client import Client
from tracker import Tracker
from pwp import PWP
import math
import uuid
import hashlib
import torrent_parser as tp
import bencode

class Peer(Server):
    """
    In this part of the peer class we implement methods to connect to multiple peers.
    Once the connection is created downloading data is done in similar way as in TCP assigment.
    """
    STATUS = ''
    ID = uuid.uuid4() # creates unique id for the peer
    INFO_HASH = ''
    SERVER_PORT = 5000
    CLIENT_MIN_PORT_RANGE = 5001
    CLIENT_MAX_PORT_RANGE = 5010
    ROUTING_TABLE = []
    PWP = ''

    def __init__(self, server_ip_address='0.0.0.0'):
        """
        Class constructor
        :param server_ip_address: used when need to use the ip assigned by LAN
        """
        Server.__init__(self, port=self.SERVER_PORT)  # inherits methods from the server
        self.read_torrent()
        self.PWP = PWP((self.length / self.piece_length), self)
        self.tracker = Tracker(self)
        self.block_index = 0
        if self.STATUS != 'seeder':
            self.connect(['127.0.0.1/5000'])

    def run_server(self):
        """
        Already implemented. puts this peer to listen for connections requests from other peers
        :return: VOID
        """
        try:
            # must thread the server, otherwise it will block the main thread
            Thread(target=self.run).start()
        except Exception as error:
            print(error)  # server failed to run

    # noinspection PyMethodMayBeStatic
    def _connect_to_peer(self, client_port_to_bind, peer_ip_address, peer_port=5000):
        """
        This method connects a client from this peer to another peer.
        :param client_port_to_bind: port to bind the client to have more control over the ports used by our P2P network
        :param peer_ip_address: the ip address of the peer
        :param peer_port: the port of the peer
        :return: True if the client connected to the Peer. Otherwise, returns False
        """
        client = Client(self)
        try:
            # binds the client to the ip address assigned by LAN
            client.bind('0.0.0.0', client_port_to_bind)  # note: when you bind, the port bound will be the client id
            self.handling_clients(client, peer_ip_address, peer_port)  # threads server
            return True
        except Exception as error:
            print(error)  # client failed to bind or connect to server
            """
              Note that the following line does not unbind the port. Sometimes, once the socket is closed 
              The port will be still bound until WAIT_TIME gets completed. If you get the error: 
              "[Errno 48] Address already in use" 
              Then, go to your terminal and do the following to unbind the port:
                  lsof -i tcp:<client_port>
              Then copy the "pid" of the process, and execute the following
                  kill -i <pid>
              There are also other ways to unbind the port in code. Try the following line in the server file right 
              after you create the server socket
                  serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
              The above line only works sometimes depending on the system and how busy is your CPU.
            """
            client.close()
            return False

    def connect(self, peers_ip_addresses):
        """
        With this function this peer creates multiple clients that connect to multiple peers
        :param peers_ip_addresses: the ip addresses of the peers (their servers ip_addresses)
        :return: VOID
        """
        client_port = self.CLIENT_MIN_PORT_RANGE
        default_peer_port = self.SERVER_PORT
        for peer_ip in peers_ip_addresses:
            if client_port > self.CLIENT_MAX_PORT_RANGE:
                break
            if "/" in peer_ip:  # checks if the ip address includes ports
                # This part is good if your P2P supports sharing different files
                # Then the same peer can run different servers in the same machine
                ip_and_port = peer_ip.split("/")
                peer_ip = ip_and_port[0]  # the ip address of the peer
                default_peer_port = int(ip_and_port[1])  # the port of the peer
            if self._connect_to_peer(client_port, peer_ip, default_peer_port):
                # the client connected. incrementing the client port here prevents
                # wasting ports in the range of ports assigned if the client connection fails.
                client_port += 1
    
    def read_torrent(self):
        with open('metainfo/age.torrent', 'rb') as torrent_file:
            torrent_data = torrent_file.read()

        torrent_data = tp.parse_torrent_file('metainfo/age.torrent')

        self.announce = torrent_data['announce']
        if self.announce == self.ip + ':' + str(self.port):
            self.STATUS = 'seeder'
        else:
            self.STATUS = 'leecher'
        self.swarm_id = torrent_data['info']['name']
        self.length = torrent_data['info']['length']
        self.piece_length = torrent_data['info']['piece length']
        self.block_length = int(self.piece_length / 8)
        sha1 = hashlib.sha1()
        sha1.update(repr(torrent_data['info']).encode('utf-8'))
        self.INFO_HASH = sha1.digest()

    def handling_clients(self, client, peer_ip_address, peer_port):
        """
        TODO: handle main services that a specific client provides such as threading the client....
        :param client:
        :return:
        """
        Thread(target=client.connect_to_server, args=(peer_ip_address, peer_port)).start()

    def routing(self, piece, swarm_id, peer_id, block):
        """
        TODO: route a piece that was received by this peer, then add that piece to the routing table
        :param piece:
        :param file_id:
        :param swarm_id:
        :return:
        """
        # Adds an entry to the routing table with the index keeping track of where the block is for retrieval
        entry = {}
        entry['peer_id'] = peer_id
        entry['swarm_id'] = swarm_id
        entry['piece_id'] = piece
        entry['block_id'] = block
        entry['index'] = self.block_index
        self.ROUTING_TABLE.append(entry)
        self.block_index += 1

    def routing_del(self, piece, swarm_id):
        for route in self.ROUTING_TABLE:
            if route['swarm_id'] == swarm_id and route['piece'] == piece:
                self.ROUTING_TABLE.delete(route)

    # Takes in a hashed piece and the index of the piece and compares it with the .torrent file.
    # If it matches, return 1, otherwise return -1
    def compare_hash(self, hash_piece, index):
        with open('metainfo/age.torrent', 'rb') as torrent_file:
            torrent_data = torrent_file.read()
        torrent = bencode.bdecode(torrent_data)
        hash = torrent['info']['pieces'][(index * 20):(index * 20 + 20)]
        print(hash)
        print(hash_piece)
        if hash == hash_piece:
            return 1
        else:
            return -1

# testing
if __name__ == "__main__":
    peer = Peer()
    print("Peer: " + str(peer.ID) + " running its server: ")
    peer.run_server()
    print("Peer: " + str(peer.ID) + " running its clients: ")