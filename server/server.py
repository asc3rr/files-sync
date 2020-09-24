import threading
import datetime
import socket
import json
import os

class Server:
    def __init__(self, settings, **kwargs):
        self.host = settings["host"]
        self.port = settings["port"]

        self.access_log = open(settings["access_log"], "w")

        self.keys = settings["keys"]
        self.max_connections = settings["max_connections"]

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

        data_to_write = f"{year}.{month}.{day} - {hour}:{minute}:{second} ~ {client_ip}"
        
        self.access_log.write(data_to_write)

    def wait_for_clients(self):
        while True:
            client, client_ip = self.server_socket.accept()

            self.update_access_log(client_ip)

            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()

        
    def handle_client(self, client):
        pass