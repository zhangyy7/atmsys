import socket

client = socket.socket()
client.connect(("localhost", 9999))

client.send(b"hello world!")
data = client.recv(1024)
print("revc:", data)

client.close()