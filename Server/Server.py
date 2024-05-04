import socket
import threading

class Server:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 4000
        self.threads = []
        self.members = []

    def test(self):
        print("Test method of server class")
        return

    def start(self):
        print("Start server!!!")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(10)

        while True:
            try:
                client_socket, address = server_socket.accept()
                thread = threading.Thread(target=self.receiver, args=(client_socket, address))
                # 데몬 스레드: start() 메소드가 끝날 경우, 스레드도 전부 종료됨.
                thread.daemon = True
                thread.start()
            except KeyboardInterrupt:
                server_socket.close()
                print("Keyboard interrupt")

    def receiver(self, client_socket, addr):
        nickname = ""
        try:
            nickname_check = False
            while not nickname_check:
                nickname = client_socket.recv(1024).decode()
                nickname_check = self.nickname_check(nickname)
                if not nickname_check:
                    client_socket.send("login:fail".encode())
            print(nickname)
            client_socket.send("login:success".encode())
            self.notify_enter(client_socket, nickname)
            while True:
                message = client_socket.recv(1024).decode()
                self.broadcast(nickname, message)
        except:
            self.notify_exit(client_socket, nickname)

    def nickname_check(self, name):
        if name == '':
            return False
        else:
            for member in self.members:
                if member[0] == name:
                    return False
            return True

    def broadcast(self, nickname, message):
        for member in self.members:
            if member[0] != nickname:
                member[1].send(f'message: {message}'.encode())

    def notify_enter(self, source, nickname):
        self.members.append((nickname, source))
        member_list = ""
        for member in self.members:
            if member[0] != nickname:
                member[1].send(f'message: {nickname} 님이 입장하셨습니다.'.encode())
            member_list += f'{member[0]};'

        self.update_members(member_list)

    def update_members(self, member_list):
        for member in self.members:
            member[1].send(f'update_members:{member_list}'.encode())
    def notify_exit(self, source, nickname):
        self.members.remove((nickname, source))
        member_list = ""
        for member in self.members:
            member_list += f'{member[0]};'
            member[1].send(f'message: {nickname} 님이 나갔습니다'.encode())

        self.update_members(member_list)