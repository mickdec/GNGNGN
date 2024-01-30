import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
s.connect(("10.129.46.139", "80"))
data = s.send(b"GET / HTTP/1.1\r\nHost:www.example.com\r\n\r\n")
data = s.recv(1024)
print(data)