import subprocess,re 
import argparse
import netaddr
import socket

#Déclaration des arguments
parser = argparse.ArgumentParser(description='Outils d\'énumeration rapide pour box/CTF.')
parser.add_argument('network', metavar='N', type=int, nargs='+',help='an integer for the accumulator')

network = "192.168.242.0/24"

def scan(ip):
    output = subprocess.run("nmap -sn "+ip,shell=True,stdout=subprocess.PIPE).stdout.decode()
    output = re.findall(r'Nmap scan report for .*',output)
    # ports = range(0,65535)
    ports = [2000]

    for elem in output:
        ip = elem.split(" ")[-1].replace("(","").replace(")","")
        print(ip + " is UP")
        for port in ports:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((ip, port))
                    data = s.recv(1024)
                    print(data)
                    print(f'{str(port)} is open.')
                except:
                    # print(f"port {str(port)} closed.")
                    continue

scan("172.16.5.0/24")
exit()


def Scan_Network(network:str):
    process = subprocess.run("nmap -sn "+network,shell=True,stdout=subprocess.PIPE)
    return process

def Scan_ip_for_port(ip):
    process = subprocess.run("nmap -p- -sV --open "+ip,shell=True,stdout=subprocess.PIPE)
    return process   

def extract_Port(text_nmap):
    return re.findall(r'(\d.*)\/tcp',text_nmap)

def Scan_port_version(ip,ports):
    command = "nmap -sV -p "
    compteur = 0
    for port in ports:
        command += port
        if compteur != len(ports)-1:
            command += ','
        compteur += 1
    command += ' '+ip
    process = subprocess.run(command,shell=True,stdout=subprocess.PIPE)
    return process

# output = Scan_Network(network).stdout.decode()
# ips = re.findall(r"(?:\d{1,3}\.){3}\d{1,3}",output)

parametre = '192.168.241.100 '
ips = list(netaddr.IPNetwork(parametre))

if len(ips) > 1:
    print("[+] Scan de l'ip :"+parametre)
    output_port = Scan_ip_for_port(parametre).stdout.decode()
else:
    print("[+] Scan du réseau :"+parametre)
    output_port = Scan_Network(parametre).stdout.decode()

ports = re.findall(r'(\d.*)\/tcp',output_port)
print(ports)
print(Scan_port_version(ips,ports=ports).stdout.decode())