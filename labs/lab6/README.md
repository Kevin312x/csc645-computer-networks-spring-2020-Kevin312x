# LAB 6: P2P BitTorrent Protocol
In last lab, students learned in detail about P2P networks and how they work. However, in order to work properly, P2P networks need to be handled by communication protocols that define what and how data is shared in the network. The BitTorrent protocol is commonly used among P2P networks because it provides good general performance. 

## How Does BitTorrent Work?

BitTorrent is a peer-to-peer protocol which means that data in a swarm is shared without the need of a central server (in theory). Traditionally, in a P2P network using the bitTorrent protocol, a computer joins the network by uploading a torrent file to the swarm.That computer becomes then part of the network (seeder). A computer that wants to download the actual file, inspect the torrent file (which contains the ip address of the tracker) and connects to the specified file. The tracker, then, sends all the ip addresses of all the computers connected to the swarm, allowing them to connect each other. It is important to point out that the tracker never has the actual files that are being shared. 

Users downloading from a bitTorrent swarm are usually refered as Lecchers and Peers. Users that remain connected to a bitTorrent swarm after the file is downloaded (seeder) contribute to the good performace of the network because they contribute to the increase of the downloading rates in the swarm. If a swarm has no seeders, then other users won´t be able to download the complete file from the swarm. That is why seeders are really important in P2P networks using the bitTorrent protocol. 

BitTorrent clients reward other clients who upload, preferring to send data to clients who contribute more upload bandwidth rather than sending data to clients who upload at a very slow speed. This speeds up download times for the swarm as a whole and rewards users who contribute more upload bandwidth.

## Trackers and Trackerless Networks 

In our definition of how a P2P network using bitTorrent protocol works, we said that it is a decentrized network in theory. Usually, that is not enterly true because there are many P2P networks that need a central server to perform some specific services in the network (i.e the tracker). One of the challenges in a decentralized bitorrent network is to make it trackerless. 

In this lab, your work is to explain in a few sentences how to make a trackerless decentralized bitTorrent network at the high level. 

### Your response here. 






