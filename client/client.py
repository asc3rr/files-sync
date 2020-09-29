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

            os.system("zip -r files *")

            file_data = open("files.zip", "rb")

            packet_data = file_data.read(50)

            while packet_data:
                print("Sending...")

                self.connection.send(packet_data)

                packet_data = file_data.read(50)

            print("Data sent")

            try:
                resp_code = self.connection.recv(1024).decode()

                if resp_code[0] == "4":
                    error_code = []
                    for i in resp_code:
                        error_code.append(i)

                    error_code.remove("4")

                    raise ErrorCode("Code: " + error_code)


            except:
                raise BadResponseError()

        else:
            raise NotConnectedError("Client not connected")

    def get_files(self):
        if self.connection:
            self.connection.send("GET".encode())

            zipped_file_conntent = self.connection.recv(1024000000).decode()

            f = open(f"{self.sync_dir}/files.zip", "w")
            f.write(zipped_file_conntent)
            f.close()

            os.system("rm *")
            os.system("rm -rf *")

            os.system("unzip files.zip")
            os.system("rm files.zip")

        else:
            raise NotConnectedError("Client not connected")

config = json.load(open("config.json"))

client = Client(config)

client.login()
client.send_files()