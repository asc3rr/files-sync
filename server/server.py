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
        self.access_log = open(config["access_log"], "w")
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

        data_to_write = f"{day}.{month}.{year} - {hour}:{minute}:{second} ~ {client_ip}"

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

            elif command == "GET":
                self.send_zip()

            else:
                client.send("403".encode())

    def get_files(self):
        #file_data = open(f"{self.dir}files.zip", "wb")
        file_data = open("test.txt", "wb")

        data = self.client.recv(50)
        print("File recieving started")

        while data:
            file_data.write(data)
            print("Got packet...")

            data = self.client.recv(50)

        print("Transfering file has ended")

        self.client.send("200".encode())

        file_data.close()

config = json.load(open("config.json"))

server = Server(config)

server.server_loop()

ClientHandler