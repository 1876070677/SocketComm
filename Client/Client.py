import socket
import threading
import time
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import sys

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.login = False
        self.nickname = ""
        self.members = []

        # GUI용 필드
        self.window = Tk()
        self.window.geometry('500x350+100+100')
        self.window.title("Kakao Talk")
        self.connect_frame = tk.Frame(self.window)
        self.connect_frame.grid(row=0, column=0, sticky='nsew')
        self.welcome_frame = tk.Frame(self.window)
        self.welcome_frame.grid(row=0, column=0, sticky='nsew')
        self.chat_frame = tk.Frame(self.window)
        self.chat_frame.grid(row=0, column=0, sticky='nsew')

        self.content_frame = tk.Frame(self.chat_frame)
        scroll = Scrollbar(self.content_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_box = tk.Listbox(self.content_frame, height=15, width=50, yscrollcommand=scroll.set)
        self.list_box.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

        self.host = StringVar()
        self.port = IntVar()
        self.user_id = StringVar()
        self.input_msg = StringVar()
        self.member_list = StringVar()

    def start(self):
        try:
            self.initialize_GUI()

        except KeyboardInterrupt:
            print("Exit!")

    def receiver(self):
        while not self.login:
            nickname_check = self.socket.recv(1024).decode()
            if 'success' == self.decode(nickname_check):
                self.login = True
            else:
                print('중복된 닉네임이 존재합니다.')

        while True:
            message = self.socket.recv(1024).decode()
            self.decode(message)

    def initialize_GUI(self):
        tk.Label(self.connect_frame, text='IP Address: ').grid(row=0, column=0, padx=5, pady=10)
        tk.Entry(self.connect_frame, textvariable=self.host).grid(row=0, column=1, padx=2, pady=10)
        tk.Label(self.connect_frame, text='Port: ').grid(row=0, column=2, padx=10, pady=5)
        tk.Entry(self.connect_frame, textvariable=self.port).grid(row=0, column=3, padx=2, pady=10)
        tk.Button(self.connect_frame, text='Connect', command=self.Connect).grid(row=0, column=4, padx=5, pady=5)
        tk.Button(self.connect_frame, text='Exit', command=self.exit).grid(row=1, column=4, padx=5, pady=5)

        tk.Label(self.welcome_frame, text='Nickname: ').grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.welcome_frame, textvariable=self.user_id).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.welcome_frame, text='Enter', command=self.Enter).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(self.welcome_frame, text='Exit', command=self.exit).grid(row=1, column=2, padx=5, pady=5)

        self.content_frame.grid(row=0, column=0)

        tk.Listbox(self.chat_frame, height=10, width=15, listvariable=self.member_list).grid(row=0, column=1, padx=5, pady=5)

        tk.Entry(self.chat_frame, width=50, textvariable=self.input_msg).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.chat_frame, text='Send', command=self.send_message).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.chat_frame, text='Exit', command=self.exit).grid(row=2, column=1, padx=5, pady=5)

        self.connect_frame.tkraise()
        self.window.mainloop()

    def Connect(self):
        if self.host.get() != "" and self.port.get() != 0:
            self.socket.connect((self.host.get(), self.port.get()))

            receiver_thread = threading.Thread(target=self.receiver)
            receiver_thread.daemon = True
            receiver_thread.start()
            self.welcome_frame.tkraise()
        else:
            messagebox.showinfo('Connect Error', '정확한 IP, Port를 입력해주세요.')

    def Enter(self):
        self.nickname = self.user_id.get()
        self.socket.send(self.nickname.encode())
        time.sleep(1.5)
        if self.login:
            self.chat_frame.tkraise()
        else:
            messagebox.showinfo('Login failed', '중복된 닉네임이 존재합니다.')

    def send_message(self):
        str = self.input_msg.get()
        if str != '':
            message = f"[{self.nickname}] {str}"
            self.socket.send(message.encode())
            self.input_msg.set("")
            self.list_box.insert(tk.END, f'Me({self.nickname}): {str}')
            self.list_box.see(tk.END)
        else:
            messagebox.showinfo('Transmission Failed', '공백 전송은 불가능합니다.')

    def decode(self, message):
        if 'login' in message:
            return message.split(":")[1]
        elif 'update_members' in message:
            members = message.split(":")[1]
            self.members = members.split(";")[:-1]
            self.member_list.set(self.members)
        elif 'message' in message:
            self.list_box.insert(tk.END, message.split(":")[1].strip())
            self.list_box.see(tk.END)
        else:
            return

    def exit(self):
        print("프로그램 종료")
        self.window.destroy()
        sys.exit(0)