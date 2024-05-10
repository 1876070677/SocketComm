import tkinter as tk
class Encoder:
    def encode(self, message, Client):
        if "/announce " in message:
            msg = f'announce:{message.split("/announce ")[1]}'
            Client.announcement.config(state=tk.NORMAL)
            Client.announcement.delete(1.0, tk.END)
            Client.announcement.insert(1.0, msg.split(":")[1])
            Client.announcement.config(state=tk.DISABLED)
            Client.input_msg.set("")
            Client.socket.send(msg.encode())
        else:
            msg = f'message:[{Client.nickname}] {message}'
            Client.socket.send(msg.encode())
            Client.input_msg.set("")
            Client.list_box.insert(tk.END, f'Me({Client.nickname}): {message}')
            Client.list_box.see(tk.END)
