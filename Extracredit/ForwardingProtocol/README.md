# The Forwarding Protocol 

As you know from class material, the network layer is organized in two sublayers: the data and control planes. Data plane refers to all the functions and processes that forward packets/frames from one interface to another.

In this project students will implement the forwarding protocol. The following are the guidelines for this project: 

* Implement input and output queues located in the input and output interfaces of the router. Note that each interface has its own input and output queues or buffers. 

* Implement priority or robin round scheduling algorithms for the input and output buffers. 

* Implement ip fragmentation so the router fabric can forward datagrams to their correspondent interface 

* Implement ip matching to select the correct interface to which datagrams need to be forwarded. 

* Implement a basic functionality to avoid loosing packets so buffers in interfaces do not drop packets 

## User Input

The user should enter the following data when the program starts:

* The source and destination ip addresses 

* The number of interfaces in the router 

* The min and max range of ip addresses for all the interfaces in the router. 

* The number of bus lines in the router fabric 

* The MTU supported by each bus line in the router fabric 

* The number of datagrams in the network

## Program Output 

The program must output in console the following data: 

* All the datagrams forwaded from input buffer to router fabric 

* The process of fragmentation inside the router fabric 

* The interface outoput selected by the program to forward the datagram from the router fabric to the output queue of that interface. 

* All the datagrams forwarded from the output buffer to the link 

## Submission Guidelines

By the due date of this project students must send an email to jortizco@sfsu.edu with the link to this project in your class repository, The email subject must be: CSC645-01 Computer Networks: EC Forwarding  

## Grading Guidelines 

Extracredit projects are all or nothing. No partial credit will be given. So, make sure that you understand the concepts presented in 
this project before doing any work. The following are the grading guidelines: 

* Provide complete documentation about the project 

* This project will be graded based on completness and correctness. 

* If I cannot run your program, I cannot grade it, and therefore, you´ll get a zero in this project. 


