# LAB 9: P2P Handling Clients and Routing Data
In this lab, students will learn about the handling and routing concepts in a P2P network and why they are so important. In lab 8, students learned about the challenges found while implementing downloading mechanismes to download data from other peers. Two of the main challenges found when downloading data from other peers are the handleing and routing processes of that data 

## Handling Clients in Peer Side

In a client-server architecture, the server handles multiple clients because those clients are sending multiple requests to that server at the same time. In a P2P network, the server side of a peer handles clients in a similar way. So, when peers request data from other peer, the server side of the peer receiving the requests handles those clients with the handler a handler function that provides all the individual functionalies for each peer trying to request data. Thus, this is the uploading process of a peer in the server side 

Handling clients in the peer side (downloading) is a bit more complicated. Imagine the following situation. P1, P2 and P3 are peers in a P2P network, and P1 is downloading data from P2 and P3. P1 has two clients sockets connected to P2 and P3 servers. Those clients are always listening for other peers responses and therefore receiving data at the same time. Handling those clients propertly is important because the peer needs to know from which swarm those clients are downloading data, and thus, routing the data to the correct file. 

## Routing Data 

Routing data is the process of routing pieces of data comming from different peers to the file they belong. This is a difficult process because those pieces of data may be being shared in different swarms. For example, P1, P2 and P3 are connected and sharing data in different swarms. When P1 receives data from P2, it needs a way of knowing to which file that piece of data belongs. The routing function is the one that perform this task. 

One way of implementing routing is to keep track of all the pieces that are being uploaded and downloaded (including the ones that are stil missing) by assigning two ID values to each message identifying the swarm and file those pieces belong to. That way those pieces can be routed to ther correspondent files once they are recieved by that peer Take into consideration that when a peer connects to a P2P network for the first time, one of the peers broadcasts to the other peers the swarnm and file IDs, so the new peers can make their own routing tables.  

## Your job in this lab 

In this lab, students will implement the basic functionality of the handling and routing functions in the Peer class. A template of the Peer class is provided in this lab, but you are free to replace it with your own Peer class from lab 8. 








