import socket
import threading
import time

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.login = False
        self.nickname = ""
        self.members = []

    def start(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))

        receiver_thread = threading.Thread(target=self.receiver, args=(client_socket, ))
        receiver_thread.start()

        sender_thread = threading.Thread(target=self.sender, args=(client_socket, ))
        sender_thread.start()

    def receiver(self, server):
        while not self.login:
            nickname_check = server.recv(1024).decode()
            if 'success' == self.decode(nickname_check):
                self.login = True
            else:
                print('중복된 닉네임이 존재합니다.')

        while True:
            message = server.recv(1024).decode()
            self.decode(message)
    def sender(self, server):
        nickname = ""
        while not self.login:
            nickname = input("Enter your nickname: ")
            if nickname != '':
                server.send(nickname.encode())
            time.sleep(2)
        self.nickname = nickname
        while True:
            str = input()
            if str != '':
                message = f"[{self.nickname}] {str}"
                server.send(message.encode())

    def decode(self, message):
        if 'login' in message:
            return message.split(":")[1]
        elif 'update_members' in message:
            members = message.split(":")[1]
            self.members = members.split(";")[:-1]
            print(self.members)
        elif 'message' in message:
            print(message.split(":")[1].strip())
        else:
            return