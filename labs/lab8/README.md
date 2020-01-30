# Lab 8: P2P Uploading and Downloading Data 
Before moving to the uploading and downloading concepts in this lab, it is important to understand that in a P2P network peers are client and servers at the same time. Once this concept is clear, we can explain how uploading and downloading works. 

## How do uploading and downloading data Work in P2P Networks? 
Uploading data to be downloaded by other peers in the network is an easy task if you understand the communication mechanisms applied to client-server sockets. However, the process of downloading data from other peers in the network is more complicated. Let´s go over both of them in detail.

### Uploading Data

In a P2P BitTorrent network, the process of a peer uploading data to other peers is similar to the client-server process where multiple clients connect to the the same server. For example, in a P2P network where peers (P1, P2 and P3) are sharing data between them and P1 is a seeder, P2 and P3 will run different clients sockets that connect to the server running in P1. As you can see, uploading data to the network is just running a server

When peers are uploading data to the network, and since they are running only one server socket, a reserved port must be assigned to such socket. Normally, the port 5000 is the one used by peers to run the server. 

### Downloading Data

Downloading data from the P2P network is a complicated process that needs a good understanding of how sockets work. Let´s explain this concept using the same network example we used in the above section. Assume like in the above section, that P1 is the seeder. Also assume that P2 downloaded some pieces of the file that P1 is sharing, and P3 wants to download those pieces from from both P1 and P2. So, P3 needs a client that must connect to the server run by P1. No problem with this configuration. However, the client from P3 also needs to connect to the server run by P2. This new configuration is not possible because the client socket that is running in P3 can only connect to one server at a time. Thus, in order to make this work, P3 needs to run two different client sockets, the first one will connect to P1´s server, and the second one will connect to P2´s server. 

So, based on the above network architecture, P2 and P3 separatelly, will run 2 client sockets and one server socket. On the other hand, P1 (the seeder) will run only one server socket and no client because the seeder does not need to download data in that specific swarm. 
It is important to point out that a seeder can be seeder in a specific swarm, but at the same time, it may be a peer in a different swarm since a swarm is sharing pnly a specific file betwwen the peers connected to it. 

One of the challenges of downloading data from other peers is to make sure that a client socket is not blocking the main thread. From other labs, we learned that in a client-server architecture clients, in the server side, need to be threaded so the main thread is not blocked. In a P2P architecture, we need to thread clients in the server side of the peer, and in the peer object itself. In addition, since we are creating many client threads in the peer object, another challenge is how to create a routing proccess to put the data from different client sockets in their correspondent file. Recall that a peer may be downloading data from different files, and be connected to different swarms at the same time. (more about this in next lab)

To sumarize, in order to be able to download data from the network, a peer needs to run several client sockets that connect to all the peer´s servers listening in the network. But, how does a peer handle all the incomming data from different servers? That peer will assign a range of ports for all the clients sockets run by the peer. For example, if a peers needs to run 5 client sockets, it will reserve ports 5001 to 5006 (both inclusive). So, a peer needs to define a range of ports for the P2P network, and a maximum number of connections to avoid taking reserved ports that are being used by other apps running in the same machine.



## Your work in this lab 

In this lab, you will implement the method connect(peers) in the Peer class template provided. This method takes as parameter a list containg all the ip addresses of the server sockets running by others peers in the swarm. Your job is to create different client sockets objects that connect to those peers. Note that in this lab, you can assume that you already have a client and server classes in the same directory as the Peer class. I am only interested here in the logic you use to implement the connect(peers) method 





