from Client import Client
if __name__ == '__main__':
    host, port = input('Enter host and port: ').split()
    client = Client.Client(host, int(port))
    client.start()