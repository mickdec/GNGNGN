import subprocess
import netaddr
import requests
import socket
from colorama import Fore, Back, Style
import time
import platform
import ssl, OpenSSL
start = time.time()
def scan(ip):
    ip_list = []
    if platform.system() == "Windows":
        output = subprocess.run("ping -n 1 -w 1 "+ip,shell=True,stdout=subprocess.PIPE).stdout.decode('utf-8',errors="ignore")
        if "perdus = 0" in output:
            ip_list.append(output.split("Ping pour ")[1].split(":")[0])
    else:
        output = subprocess.run("ping -c 1 -t 1 "+ip,shell=True,stdout=subprocess.PIPE).stdout.decode('utf-8',errors="ignore")
        if "0% packet loss" in output:
            ip_list.append(output.split("PING ")[1].split(" (")[0])
    ports = range(0,65535)
    for ip in ip_list:
        print(ip + " is UP")
        for port in ports:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(.1)
                    s.connect((ip, port))
                except:
                    print(port)
                    continue
                dataset = s.send(b"GET / HTTP/1.1\r\nHost:127.0.0.1\r\n\r\n")
                dataset_undecoded = s.recv(1024)
                dataset = dataset_undecoded.decode().replace("\r\n\r\n","\r\n")
                if dataset[-1] == "\n":
                    dataset = dataset[:-1]
                if dataset[-1] == "\r":
                    dataset = dataset[:-1]
                dataset_list = dataset.split("\r\n")
                print(f'{Back.GREEN + str(port) + Style.RESET_ALL} is open.')
                ishttp = 0
                for data in dataset_list:
                    if "HTTP/1" in data:
                        ishttp = 1
                        print(data,end=" - ")
                        for data in dataset_list:
                            if "Server: " in data:
                                server = data.replace("Server: ","")
                                print(server)
                if ishttp:
                    URL_DNS = f"https://{ip}:{port}/"
                    try:
                        cert = ssl.get_server_certificate((URL_DNS, 443))
                        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
                        for comp in x509.get_subject().get_components():
                            for xcomp in comp:
                                if xcomp.decode() == "CN":
                                    hostname = comp[1].decode()
                    except:
                        hostname = "Inconnu"
                    print("Hostname : " + hostname)
                else:
                    if "\\x" in str(dataset_undecoded):
                        print(dataset_undecoded)
                    else:
                        print(dataset)

scan("200.54.253.65")
print("Durée du scan " + str(time.time() - start)[:-13])
exit()