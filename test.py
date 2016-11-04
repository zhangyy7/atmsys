import socket

server = socket.socket()
server.bind(("localhost", 9999))
server.listen()

print("我要开始等电话了")
conn, addr = server.accept()
print(conn, addr)
print("我要开始等电话了")
data = conn.recv(1024)
conn.send(data.upper())

server.close()
