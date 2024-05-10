import tkinter as tk
class Decoder:
    def decode(self, message, Client):
        if 'login' in message:
            if message.split(":")[1] == 'success':
                Client.login = True
        elif 'update_members' in message:
            members = message.split(":")[1]
            Client.members = members.split(";")[:-1]
            Client.member_list.set(Client.members)
        elif 'announce' in message:
            Client.announcement.config(state=tk.NORMAL)
            Client.announcement.delete(1.0, tk.END)
            Client.announcement.insert(1.0, message.split(":")[1])
            Client.announcement.config(state=tk.DISABLED)
        elif 'message' in message:
            Client.list_box.insert(tk.END, message.split(":")[1].strip())
            Client.list_box.see(tk.END)