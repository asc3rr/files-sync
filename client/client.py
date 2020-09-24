import socket
import json
import os

class LoginError(Exception):
    pass

class Client:
    def __init__(self, settings):
        self.host = settings["host"]
        self.port = settings["port"]
        self.key = settings["key"]

        self.connection = None

    def login(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.host, self.port))

        conn.send(self.key.encode())

        resp = conn.recv(1024)

        if resp == "200":
            self.connection = conn

        else:
            raise LoginError("Login failed.")

    def send_data(self, data:str):
        self.connection.send(data.encode())

    def get_response(self):
        response = self.connection.recv(1024).decode()

        return response

settings = json.load(open("settings.json"))

client = Client(settings)
client.login()