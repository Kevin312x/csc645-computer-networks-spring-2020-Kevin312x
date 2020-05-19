from server import Server

class Tracker(Server):
    PEERS = []

    def __init__(self, Server):
        self = Server

    def addPeer(self, peer_ip_address, peer_port, clientsocket):
        peer = peer_ip_address + '/' + str(peer_port)
        # CAN'T SEND SOCKET OBJECTS
        # data = { 'peer': peer, 'clientsocket': clientsocket }
        data = {'peer': peer}
        self.PEERS.append(data)

    def sendPeersIPAddress(self):
        # for peer in self.PEERS:
        #     data = {'id': 'tracker', 'tracker': self.PEERS}
        #     self._send(peer['clientsocket'], data)
        pass