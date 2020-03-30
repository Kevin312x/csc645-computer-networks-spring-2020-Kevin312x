#######################################################################
# File:             client_handler.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template ClientHandler class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client handler class, and use a version of yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################
import pickle
import threading
from menu import Menu

class ClientHandler(object):
    """
    The ClientHandler class provides methods to meet the functionality and services provided
    by a server. Examples of this are sending the menu options to the client when it connects,
    or processing the data sent by a specific client to the server.
    """
    def __init__(self, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you
        :param server_instance: normally passed as self from server object
        :param clientsocket: the socket representing the client accepted in server side
        :param addr: addr[0] = <server ip address> and addr[1] = <client id>
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.clientsocket = clientsocket
        self.server.send_client_id(self.clientsocket, self.client_id)
        self.unreaded_messages = []
        self.chatroom = None
        self.server.clients[self.client_id] = self

        client_name = self.server.receive(self.clientsocket)
        self.name = client_name['client_name']

        self._sendMenu()
        self.process_options()

    def _sendMenu(self):
        """
        Already implemented for you.
        sends the menu options to the client after the handshake between client and server is done.
        :return: VOID
        """
        menu = Menu()
        data = {'menu': menu}
        self.server.send(self.clientsocket, data)

    def process_options(self):
        """
        Process the option selected by the user and the data sent by the client related to that
        option. Note that validation of the option selected must be done in client and server.
        In this method, I already implemented the server validation of the option selected.
        :return:
        """
        while True:
            data = self.server.receive(self.clientsocket)
            if 'option' in data.keys() and 1 <= data['option'] <= 6: # validates a valid option selected
                option = data['option']
                if option == 1:
                    self._send_user_list()
                elif option == 2:
                    recipient_id = data['recipient_id']
                    message = data['message']
                    self._save_message(recipient_id, message)
                elif option == 3:
                    self._send_messages()
                elif option == 4:
                    room_id = data['room_id']
                    self._create_chat(room_id)
                elif option == 5:
                    room_id = data['room_id']
                    self._join_chat(room_id)
                elif option == 6:
                    self._disconnect_from_server()
                    break
            else:
                print("The option selected is invalid")

    def _send_user_list(self):
        """
        TODO: send the list of users (clients ids) that are connected to this server.
        :return: VOID
        """
        data = {}
        clients = ""
        for obj in self.server.clients:
            clients += self.server.clients[obj].name + ':' + str(self.server.clients[obj].client_id)
            clients += ", "
        
        data['clients'] = clients[:-2]
        self.server.send(self.clientsocket, data)


    def _save_message(self, recipient_id, message):
        """
        TODO: link and save the message received to the correct recipient. handle the error if recipient was not found
        :param recipient_id:
        :param message:
        :return: VOID
        """
        self.server.clients[recipient_id].unreaded_messages.append(message)
        

    def _send_messages(self):
        """
        TODO: send all the unreaded messages of this client. if non unread messages found, send an empty list.
        TODO: make sure to delete the messages from list once the client acknowledges that they were read.
        :return: VOID
        """
        data = {}
        data['messages'] = '\n'.join(self.unreaded_messages)
        self.server.send(self.clientsocket, data)
        self.unreaded_messages = []
        

    def _create_chat(self, room_id):
        """
        TODO: Creates a new chat in this server where two or more users can share messages in real time.
        :param room_id:
        :return: VOID
        """
        data = {}
        flag = True
        for obj in self.server.clients:
            if self.server.clients[obj].chatroom != None and self.server.clients[obj].chatroom.room_id == room_id:
                flag = False

        if flag == True:
            self.chatroom = Chatroom(self.client_id, room_id)
            data['created'] = True
            data['room_id'] = room_id
            data['chatroom'] = self.chatroom
            self.server.send(self.clientsocket, data)
        else:
            data['created'] = False
            self.server.send(self.clientsocket, data)

        while self.chatroom != None:
            msg = self.server.receive(self.clientsocket)
            if not msg:
                break
            sender_id = msg['sender_id']
            message = msg['message']
            room_id = msg['chatroom_id']
            self.process_chat_messages(sender_id, message, room_id)
            if 'exit' in message.lower():
                self.chatroom = None
                break
        

    def _join_chat(self, room_id):
        """
        TODO: join a chat in a existing room
        :param room_id:
        :return: VOID
        """
        data = {}
        flag = False
        chatrm = None
        for obj in self.server.clients:
            if self.server.clients[obj].chatroom != None and self.server.clients[obj].chatroom.room_id == room_id:
                flag = True
                chatrm = self.server.clients[obj].chatroom
        
        if flag == True:
            self.chatroom = chatrm
            data['joined'] = True
            data['room_id'] = room_id
            data['chatroom'] = self.chatroom
            self.server.send(self.clientsocket, data)
        else:
            data['joined'] = False
            self.server.send(self.clientsocket, data)

        while self.chatroom != None:
            msg = self.server.receive(self.clientsocket)
            if not msg:
                break
            sender_id = msg['sender_id']
            message = msg['message']
            room_id = msg['chatroom_id']
            self.process_chat_messages(sender_id, message, room_id)
            if 'bye' in message.lower():
                self.chatroom = None
                break
        

    def delete_client_data(self):
        """
        TODO: delete all the data related to this client from the server.
        :return: VOID
        """
        for obj in self.server.clients:
            if self.server.clients[obj].client_id == self.client_id:
                del self.server.clients[obj]
                break

    def _disconnect_from_server(self):
        """
        TODO: call delete_client_data() method, and then, disconnect this client from the server.
        :return: VOID
        """
        self.delete_client_data()
        data = {}
        data['close'] = True
        self.server.send(self.clientsocket, data)


    def process_chat_messages(self, sender_id, message, room_id):
        for obj in self.server.clients:
            if self.server.clients[obj].chatroom != None:
                if self.server.clients[obj].chatroom.room_id == room_id:
                    data = {}
                    if self.server.clients[obj].client_id == sender_id:
                        data['self'] = True
                    else:
                        data['self'] = False
                    if self.server.clients[obj].chatroom.owner_id == self.client_id:
                        data['status'] = 'owner'
                    else:
                        data['status'] = 'user'
                    data['messages'] = message
                    self.server.send(self.server.clients[obj].clientsocket, data)


class Chatroom(object):

    def __init__(self, owner_id, room_id):
        self.owner_id = owner_id
        self.room_id = room_id
        self.users = [owner_id]