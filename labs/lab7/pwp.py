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
    choke = 0
    unchoke = 1
    interested = 2
    not_interested = 3
    have = 4
    bitfield = 5
    request = 6
    piece = 7
    cancel = 8

    def __init__(self):
        """
        Empty constructor
        """
        self.message = Message()
        self.message.init_bitfield(num_pieces)

    def handshake(self, info_hash, peer_id, pstrlen=PSTRLEN, pstr=PSTR):
        """
        TODO: implement the handshake
        :param options:
        :return: the handshake message
        """
        return bencode.encode(chr(pstrlen) + pstr + (8 * chr(0)) + info_hash + peer_id)

    def message(self, len, message_id, payload):
        """
        TODO: implement the message
        :param len:
        :param message_id:
        :param payload:
        :return: the message
        """
        return bencode.encode(len + chr(message_id) + self.payload(id))

    def payload(self, message_id):
        if(message_id == self.have):
            return (self.message.chr(have['piece_index']))
        
        elif(message_id == self.bitfield):
            bits = ''
            for i in self.message._bitfield['bitfield']:
                bits += ''.join(str(j) for j in i)
            
            return bencode.encode(bits)
        
        elif(message_id == self.request or message_id == self.cancel):
            return chr(self.message.request['index']) + chr(self.message.request['begin']) + chr(self.message.request['length'])
        
        elif(message_id == self.piece):
            return chr(self.message.piece['index']) + chr(self.message.piece['begin']) + chr(self.message.piece['block'])
        
        else:
            return ''