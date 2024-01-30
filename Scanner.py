import subprocess,re 
import argparse
import netaddr
import socket
from colorama import Fore, Back, Style

#Déclaration des arguments
parser = argparse.ArgumentParser(description='Outils d\'énumeration rapide pour box/CTF.')
parser.add_argument('network', metavar='N', type=int, nargs='+',help='an integer for the accumulator')

def scan(ip):
    output = subprocess.run("nmap -sn "+ip,shell=True,stdout=subprocess.PIPE).stdout.decode()
    output = re.findall(r'Nmap scan report for .*',output)
    ports = range(0,65535)
    for elem in output:
        ip = elem.split(" ")[-1].replace("(","").replace(")","")
        print(ip + " is UP")
        for port in ports:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((ip, port))
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
                            print("HTTP Server - ",end="")
                    if dataset == "":
                        dataset = "EMPTY RESPONSE."
                    print(dataset_undecoded)
                        
                except:
                    continue
scan("127.0.0.1")
exit()