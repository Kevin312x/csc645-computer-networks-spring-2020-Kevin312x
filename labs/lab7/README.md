# Lab 7, P2P: The BitTorrent Peer Wire Protocol 
In this lab, you´ll create a Python class that implements the services provided by the Peer Wire Protocol. 

## How Does it work?

The Peer Wire Protocol defines the form of the communication between peers in the network. The peer wire protocol consists of an initial handshake. After that, peers communicate via an exchange of length-prefixed messages. The length-prefix is an integer representing a sequence of bytes

## Handshake

The handshake is a required message and must be the first message transmitted by the client. It is (49+len(pstr)) bytes long.

handshake: <pstrlen><pstr><reserved><info_hash><peer_id>

pstrlen: string length of <pstr>, as a single raw byte
  
pstr: string identifier of the protocol

reserved: eight (8) reserved bytes. All current implementations use all zeroes. Each bit in these bytes can be used to change the behavior of the protocol. 

info_hash: 20-byte SHA1 hash of the info key in the metainfo file. This is the same info_hash that is transmitted in tracker requests.

peer_id: 20-byte string used as a unique ID for the client. This is usually the same peer_id that is transmitted in tracker requests 

In version 1.0 of the BitTorrent protocol, pstrlen = 19, and pstr = "BitTorrent protocol"

### Peer Messages

All non-keepalive messages start with a single byte which gives their type.

The possible values are:

0 - choke

1 - unchoke

2 - interested

3 - not interested

4 - have

5 - bitfield

6 - request

7 - piece

8 - cancel

'choke', 'unchoke', 'interested', and 'not interested' have no payload

All of the remaining messages in the protocol take the form of <length prefix><message ID><payload>. The length prefix is a four byte big-endian value. The message ID is a single decimal byte. The payload is message dependent.

### keep-alive: <len=0000>
The keep-alive message is a message with zero bytes, specified with the length prefix set to zero. There is no message ID and no payload. Peers may close a connection if they receive no messages (keep-alive or any other message) for a certain period of time, so a keep-alive message must be sent to maintain the connection alive if no command have been sent for a given amount of time. This amount of time is generally two minutes.

### choke: <len=0001><id=0>
The choke message is fixed-length and has no payload.

### unchoke: <len=0001><id=1>
The unchoke message is fixed-length and has no payload.

### interested: <len=0001><id=2>
The interested message is fixed-length and has no payload.

### not interested: <len=0001><id=3>
The not interested message is fixed-length and has no payload.

### have: <len=0005><id=4><piece index>
The have message is fixed length. The payload is the zero-based index of a piece that has just been successfully downloaded and verified via the hash.

Implementer's Note: That is the strict definition, in reality some games may be played. In particular because peers are extremely unlikely to download pieces that they already have, a peer may choose not to advertise having a piece to a peer that already has that piece. At a minimum "HAVE suppression" will result in a 50% reduction in the number of HAVE messages, this translates to around a 25-35% reduction in protocol overhead. At the same time, it may be worthwhile to send a HAVE message to a peer that has that piece already since it will be useful in determining which piece is rare.

A malicious peer might also choose to advertise having pieces that it knows the peer will never download. Due to this attempting to model peers using this information is a bad idea.

### bitfield: <len=0001+X><id=5><bitfield>
The bitfield message may only be sent immediately after the handshaking sequence is completed, and before any other messages are sent. It is optional, and need not be sent if a client has no pieces.

The bitfield message is variable length, where X is the length of the bitfield. The payload is a bitfield representing the pieces that have been successfully downloaded. The high bit in the first byte corresponds to piece index 0. Bits that are cleared indicated a missing piece, and set bits indicate a valid and available piece. Spare bits at the end are set to zero.

Some clients (Deluge for example) send bitfield with missing pieces even if it has all data. Then it sends rest of pieces as have messages. They are saying this helps against ISP filtering of BitTorrent protocol. It is called lazy bitfield.

A bitfield of the wrong length is considered an error. Clients should drop the connection if they receive bitfields that are not of the correct size, or if the bitfield has any of the spare bits set.

### request: <len=0013><id=6><index><begin><length>
The request message is fixed length, and is used to request a block. The payload contains the following information:

index: integer specifying the zero-based piece index

begin: integer specifying the zero-based byte offset within the piece

length: integer specifying the requested length

### piece: <len=0009+X><id=7><index><begin><block>
The piece message is variable length, where X is the length of the block. The payload contains the following information:

index: integer specifying the zero-based piece index

begin: integer specifying the zero-based byte offset within the piece

block: block of data, which is a subset of the piece specified by index.

### cancel: <len=0013><id=8><index><begin><length>
The cancel message is fixed length, and is used to cancel block requests. The payload is identical to that of the "request" message
