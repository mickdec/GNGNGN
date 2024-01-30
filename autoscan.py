import subprocess,re 

network = "192.168.242.0/24"

def Scan_Network(network:str):
    process = subprocess.run("nmap -sn "+network,shell=True,stdout=subprocess.PIPE)

    return procses

def Scan_ip_for_port(ip):
    process = subprocess.run("nmap -p- "+ip,shell=True,stdout=subprocess.PIPE)
    
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

ips = ['192.168.241.213']
for ip in ips:
    output_port = (Scan_ip_for_port(ip).stdout.decode())
    ports = re.findall(r'(\d.*)\/tcp',output_port)
    print(ports)
    print(Scan_port_version(ip,ports=ports).stdout.decode())