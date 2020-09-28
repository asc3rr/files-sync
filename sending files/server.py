import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 1024))
s.listen(10)

file_data = open("data_recvd.txt", "w")

client, address = s.accept()

print(f"Connection from {address}")

print("File recieving started...")

data = client.recv(1024)

while data:
    file_data.write(data.decode())
    print("Got packet...")

    data = client.recv(1024)

print("Transfering file has ended")

client.close()
file_data.close()