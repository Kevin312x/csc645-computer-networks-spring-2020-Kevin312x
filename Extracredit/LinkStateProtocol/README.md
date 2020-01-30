# Link State Protocol 

As you may know from class lectures, there are two routing algorithms that operate in the network layer, the link state and the distance vector protocols. The link state routing protocol is a routing algorithm that creates routing tables for all the routers in the network. Such routing tables contain the shortest path from source to destination. The distance vector routing algorithm updates the routing tables of all the routers in the network everytime a path in the network changes. In this extracredit assignment, students will implement the link state routing protocol.

## User Input 

This program needs the following data from the user: 

1. The nodes in the network. 

       > Enter the nodes in the network: x y z 
       
2. The paths between such nodes 

       > Enter the paths between nodes: (x, y, 12) (y, z, 34) (z, x, 78) 
       
## Program output 

The ouput of the program is the routing table that all the routers will hold after the algorithm is done. Like in the example in class slides. 

