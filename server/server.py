import threading
import datetime
import socket
import json
import os

class Server:
    def __init__(self, config):
        self.host = config["host"]
        self.port = config["port"]
        self.keys = config["keys"]

        self.max_connections = config["max_connections"]
        self.access_log = open(config["access_log"], "a")
        self.dir = config["dir"]
        
        self.server_socket = None

        ### Setting up sockets
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_connections)

        print(f"Server hosted on {self.host}:{self.port}")

    def update_access_log(self, client_ip):
        now = datetime.datetime.now()

        year = now.year
        month = now.month
        day = now.day

        hour = now.hour
        minute = now.minute
        second = now.second

        data_to_write = f"{day}.{month}.{year} - {hour}:{minute}:{second} ~ {client_ip}\n"

        self.access_log.write(data_to_write)

    def server_loop(self):
        while True:
            client, address = self.server_socket.accept()

            self.update_access_log(address)

            given_key = client.recv(1024).decode()

            is_key_valid = False

            for key in self.keys:
                if given_key == key:
                    is_key_valid = True
                    client.send("200".encode())

            if not is_key_valid:
                client.close()

            client_thread = threading.Thread(target=ClientHandler, args=(client, self.dir))
            client_thread.start()

class ClientHandler: 
    def __init__(self, client, sync_dir):
        self.dir = sync_dir
        self.client = client

        while True:
            command = client.recv(1024).decode()

            if command == "FILES":
                self.get_files()
                self.client.close()

            elif command == "GET":
                self.send_files()

            else:
                client.send("403".encode())

    def get_files(self):
        #file_data = open(f"{self.dir}files.zip", "wb")
        file_data = open("files.zip", "wb")

        data = self.client.recv(1024)

        while data:
            file_data.write(data)

            data = self.client.recv(1024)

        self.client.send("200".encode())

        self.client.close()
        file_data.close()

    def send_files(self):
        file_data = open("files.zip", "rb")

        packet_data = file_data.read(1024)

        while packet_data:
            self.client.send(packet_data)

            packet_data = file_data.read(1024)

        self.client.close()
        file_data.close()

config = json.load(open("config.json"))

server = Server(config)

server.server_loop()
