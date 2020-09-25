import threading
import datetime
import socket
import json
import os

class Server:
    def __init__(self, config):
        self.host = config["host"]
        self.port = config["port"]
        self.keys = config["key"]

        self.max_connections = config["max_connections"]
        self.access_log = open(config["access_log"], "w")
        self.dir = config["dir"]
        
        self.server_socket = None

        ### Setting up sockets
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_connections)

    def update_access_log(self, client_ip):
        now = datetime.datetime.now()

        year = now.year
        month = now.month
        day = now.day

        hour = now.hour
        minute = now.minute
        second = now.second

        data_to_write = f"{day}.{month}.{year} - {hour}:{minute}:{second} ~ {client_ip}"

        self.access_log.write(data_to_write)

    def server_loop(self):
        while True:
            client, address = self.server_socket.accept()

            self.update_access_log(address)

            given_key = self.server_socket.recv(1024).decode()

            is_key_valid = False

            for key in self.keys:
                if given_key == key:
                    is_key_valid = True
                    client.send("200".encode())

            if not is_key_valid:
                client.close()

            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()

    def handle_client(self, client):
        while True:
            command = client.recv(1024).decode()

            if command == "FILES":
                pass

            elif command == "GET":
                pass

            else:
                client.send("403".encode())