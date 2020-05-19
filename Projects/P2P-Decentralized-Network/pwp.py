"""
Lab 7: Peer Wire Protocol (PWP)
Create a class with the basic implementation for the bitTorrent peer wire protocol
A basic template structure is provided, but you may need to implement more methods
For example, the payload method depending of the option selected
"""

from message import Message
import bencode

class PWP(object):
    # pstr and pstrlen constants used by the handshake process
    PSTR = "BitTorrent protocol"
    PSTRLEN = 19
    # TODO: Define ID constants for all the message fields such as unchoked, interested....
    CHOKE = 0
    UNCHOKE = 1
    INTERESTED = 2
    NOT_INTERESTED = 3
    HAVE = 4
    BITFIELD = 5
    REQUEST = 6
    PIECE = 7
    CANCEL = 8

    def __init__(self, num_pieces, peer):
        """
        Empty constructor
        """
        self.msg = Message(peer)
        self.msg.init_bitfield(num_pieces)

    def handshake(self, info_hash, peer_id, pstrlen=PSTRLEN, pstr=PSTR):
        """
        TODO: implement the handshake
        :param options:
        :return: the handshake message
        """
        return {'info_hash': info_hash, 'peer_id': peer_id, 'pstrlen': pstrlen, 'pstr': pstr}

    def _message(self, payload=None, message_id=-1, len_hex=b'00009'):
        """
        TODO: implement the message
        :param len_hex: the len_hex is passed of the id is 7 because the message is variable in len
        :param message_id: the id of the message
        :param payload:the payload contains all the basic info that needs to be sent to the other peer
        :return: returns the message based on the message_id and payload. If no message_id and no payload then
                 returns the keep_alive message. The keep_alive will keep the connection alive between peers for
                 about two minutes until another message is sent, otherwise the connection will be closed by the
                 other peer.
        """
        if message_id == 0:
            return self.msg.choke
        elif message_id == 1:
            return self.msg.unchoke
        elif message_id == 2:
            return self.msg.interested
        elif message_id == 3:
            return self.msg.not_interested
        elif message_id == 4:
            return self.msg.get_have(payload)
        elif message_id == 5:
            return self.msg.get_bitfield()  # sent immediately after the Handshake
        elif message_id == 6:
            return self.msg.get_request(payload)
        elif message_id == 7:
            return self.msg.get_piece(payload, len_hex)
        elif message_id == 8:
            return self.msg.get_cancel(payload)
        elif message_id == 9:
            return self.msg.get_port(payload)
        elif message_id == 10:
            return self.msg.get_tracker(payload)
        return self.msg.keep_alive