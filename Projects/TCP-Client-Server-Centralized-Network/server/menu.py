#######################################################################################
# File:             menu.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template Menu class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this Menu class, and use a version of yours instead.
# Important:        The server sends a object of this class to the client, so the client is
#                   in charge of handling the menu. This behaivor is strictly necesary since
#                   the client does not know which services the server provides until the
#                   clients creates a connection.
# Running:          This class is dependent of other classes.
# Usage :           menu = Menu() # creates object
#
########################################################################################
from datetime import datetime
import threading

class Menu(object):
    """
    This class handles all the actions related to the user menu.
    An object of this class is serialized ans sent to the client side
    then, the client sets to itself as owner of this menu to handle all
    the available options.
    Note that user interactions are only done between client and user.
    The server or client_handler are only in charge of processing the
    data sent by the client, and send responses back.
    """

    def __init__(self):
        """
        Class constractor
        :param client: the client object on client side
        """
        #self.client = client

    def set_client(self, client):
        self.client = client

    def show_menu(self):
        """
        TODO: 1. send a request to server requesting the menu.
        TODO: 2. receive and process the response from server (menu object) and set the menu object to self.menu
        TODO: 3. print the menu in client console.
        :return: VOID
        """
        self.menu = self.get_menu()
        print(self.menu)
        

    def process_user_data(self):
        """
        TODO: according to the option selected by the user, prepare the data that will be sent to the server.
        :param option:
        :return: VOID
        """
        while True:
            self.show_menu()
            data = {}
            option = self.option_selected()
            if 1 <= option <= 6: # validates a valid option
                # TODO: implement your code here
                if option == 1:
                    data = self.option1()
                    self.client.send(data)
                    lists = self.client.receive()
                    print("Users in server:",lists['clients'])
                elif option == 2:
                    data = self.option2()
                    self.client.send(data)
                    print("Message sent!")
                elif option == 3:
                    data = self.option3()
                    self.client.send(data)
                    print("My messages:")
                    lists = self.client.receive()
                    print(lists['messages'])
                elif option == 4:
                    data = self.option4()
                    self.client.send(data)
                    created = self.client.receive()
                    status = created['created']
                    if status == True:
                        self.chatroom = created['chatroom']
                        user_status = 'owner'
                        print("-----------------------", "Chat Room" , data['room_id'], "------------------------")
                        print("Type 'exit' to close the chat room")
                        print("Chat room created by:", self.client.name)
                        print("Waiting for other users to join....")

                        recv_thread = threading.Thread(target=self.recv, args=(user_status,))
                        recv_thread.start()

                        while True:
                            input_data = {}
                            message = input()
                            lock = self.print_lock()
                            lock.acquire()
                            message = self.client.name + '> ' + message
                            input_data['message'] = message
                            input_data['sender_id'] = self.client.client_id
                            input_data['chatroom_id'] = self.chatroom.room_id
                            self.client.send(input_data)
                            lock.release()
                            if 'exit' in message.lower():
                                stop_thread = True
                                recv_thread.join()
                                break

                    else:
                        print("Room id is already taken")

                elif option == 5:
                    data = self.option5()
                    self.client.send(data)
                    joined = self.client.receive()
                    status = joined['joined']

                    if status == True:
                        self.chatroom = joined['chatroom']
                        user_status = 'user'
                        loop = True
                        print("-----------------------", "Chat Room" , joined['room_id'], "------------------------")
                        print("Joined to chat room", joined['room_id'])
                        print("Type 'bye' to exit this chat room")
                        data = {}
                        data['sender_id'] = self.client.client_id
                        data['message'] = self.client.name + " joined"
                        data['chatroom_id'] = self.chatroom.room_id
                        self.client.send(data)

                        recv_thread = threading.Thread(target=self.recv, args=(user_status,))
                        recv_thread.start()

                        while loop:
                            input_data = {}
                            message = input()
                            message = self.client.name + '> ' + message
                            input_data['message'] = message
                            input_data['sender_id'] = self.client.client_id
                            input_data['chatroom_id'] = self.chatroom.room_id
                            self.client.send(input_data)
                            if 'bye' in message.lower():
                                stop_thread = True
                                break

                    else:
                        print("Room id doesn't exist")

                elif option == 6:
                    data = self.option6()
                    self.client.send(data)
                    self.client.receive()
                    self.client.close()
                    break
    
            # (i,e  algo: if option == 1, then data = self.menu.option1, then. send request to server with the data)
        


    def option_selected(self):
        """
        TODO: takes the option selected by the user in the menu
        :return: the option selected.
        """
        option = 0
        # TODO: your code here.
        option = input("Your option <enter a number>: ")
        return int(option)

    def get_menu(self):
        """
        TODO: Implement the following menu
        ****** TCP CHAT ******
        -----------------------
        Options Available:
        1. Get user list
        2. Send a message
        3. Get my messages
        4. Create a new channel
        5. Chat in a channel with your friends
        6. Disconnect from server
        :return: a string representing the above menu.
        """
        menu = '''
        ****** TCP CHAT ******
        -----------------------
        Options Available:
        1. Get user list
        2. Send a message
        3. Get my messages
        4. Create a new channel
        5. Chat in a channel with your friends
        6. Disconnect from server
        '''
        # TODO: implement your code here
        return menu

    def option1(self):
        """
        TODO: Prepare the user input data for option 1 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 1.
        """
        data = {}
        data['option'] = 1
        # Your code here.
        return data

    def option2(self):
        """
        TODO: Prepare the user input data for option 2 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 2.
        """
        data = {}
        data['option'] = 2
        # Your code here.
        date_time = datetime.now()
        date = date_time.date()
        time = date_time.time().strftime("%H:%M")
        message = input("Enter your message: ")
        r_id = input("Enter recipient id: ")
        data['message'] = str(date) + ' ' + time + ' ' + message
        data['recipient_id'] = int(r_id)
        return data

    def option3(self):
        """
        TODO: Prepare the user input data for option 3 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 3.
        """
        data = {}
        data['option'] = 3
        # Your code here.
        return data

    def option4(self):
        """
        TODO: Prepare the user input data for option 4 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 4.
        """
        data = {}
        data['option'] = 4
        # Your code here.
        room_id = input("Enter a new chat room id: ")
        data['room_id'] = room_id
        data['owner'] = self.client.client_id
        return data


    def option5(self):
        """
        TODO: Prepare the user input data for option 5 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 5.
        """
        data = {}
        data['option'] = 5
        # Your code here.
        room_id = input("Enter chat room id to join: ")
        data['room_id'] = room_id
        return data

    def option6(self):
        """
        TODO: Prepare the user input data for option 6 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 6.
        """
        data = {}
        data['option'] = 6
        # Your code here.
        return data

    def recv(self, user_status):
        while True:
            lock = self.print_lock()
            msg = self.client.receive()
            lock.acquire()
            message = msg['messages']
            sender_self = msg['self']
            status = msg['status']
            if sender_self:
                if 'exit' in message.lower() and status == 'owner':
                    break
                elif 'bye' in message.lower() and status == 'user':
                    break
            else:
                print(message)
            lock.release()

    
    def print_lock(self):
        return threading.Lock()