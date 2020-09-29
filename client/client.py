import socket
import json
import os

class LoginError(Exception):
    """Access denied"""
    pass

class NotConnectedError(Exception):
    """Client is not connected"""
    pass

class BadResponseError(Exception):
    """Response is not expected"""
    pass

class ErrorCode(Exception):
    """Response Codes"""
    pass

class Client:
    def __init__(self, config):
        self.host = config["host"]
        self.port = config["port"]
        self.key = config["key"]

        self.sync_dir = config["sync_dir"]

        self.connection = None

    def login(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.host, self.port))

        conn.send(self.key.encode())

        resp = conn.recv(1024).decode()

        if resp == "200":
            self.connection = conn

        else:
            raise LoginError("Access denied.")

    def send_files(self):
        if self.connection:
            self.connection.send("FILES".encode())

            os.system(f"zip -r files {self.sync_dir}*")

            file_data = open("files.zip", "rb")

            packet_data = file_data.read(50)

            while packet_data:
                print("Sending...")

                self.connection.send(packet_data)

                packet_data = file_data.read(50)

            print("Data sent")

        else:
            raise NotConnectedError("Client not connected")

    def get_files(self):
        if self.connection:
            self.connection.send("GET".encode())

            file_data = open("files.zip", "wb")

            data = self.connection.recv(50)
            print("File recieving started")

            while data:
                file_data.write(data)
                print("Got packet...")

                data = self.connection.recv(50)

            print("Transfering file has ended")

            file_data.close()

        else:
            raise NotConnectedError("Client not connected")

config = json.load(open("config.json"))

client = Client(config)

client.login()
client.get_files()