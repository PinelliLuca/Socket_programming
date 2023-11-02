import socket
import sys
import time
import ipaddress
import json

#funzione che controlla che il formato del CIDR sia valido
def controllo_ip(data):
    try:
        ipaddress.IPv4Network(data, strict=False)
        return True
    except ValueError:
        return False

#funzione che calcola l'ip minimo e massimo tranne l'indirizzo di broadaast e di rete
def MinMaxIp(netid, netmask):
    network = ipaddress.IPv4Network(f'{netid}/{netmask}', strict=False)
    ip_min = network.network_address + 1
    ip_max = network.broadcast_address - 1
    return str(ip_min), str(ip_max)


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8080        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
   
    data = conn.recv(1024).decode('utf-8')
    data = json.loads(data)
    if( not data):
        print("Errore: Dati errati inviati al server")

    netid,netmask = data.split('/')
    if(not netid or not netmask):
        risp= {"status":"ERROR"}
    elif(controllo_ip(f'{netid}/{netmask}')==True):
        ip_min,ip_max = MinMaxIp(netid,netmask)
        risp = {"status":"OK","IPmin":ip_min,"IPmax":ip_max}
    else:
        risp = {"status":"ERROR2"}
    risp = json.dumps(risp)
    conn.sendall(risp.encode('utf-8'))
    # socket must be closed by client! sleep for 1 second to wait for the client
    time.sleep(1)
    # otherwise socket goes to TIME_WAIT!

