import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1024))

file_data = open("data_to_send.txt")

packet_data = file_data.read(1024)

while packet_data:
    print("Sending...")

    s.send(packet_data.encode())

    packet_data = file_data.read(1024)

print("Data sent")