#!/usr/bin/env python3
#dato un indirizzo dal client il server ritorni la classe, il broadcast e il netid
import socket
import sys
import time
import ipaddress

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 1025       # Port to listen on (non-privileged ports are > 1023)

def ip_class(ip):
    ip = ip.split('.')
    parte = int(ip[0])
    if parte >= 1 and parte <= 127:
        return 'A'
    elif parte >= 128 and parte <= 191:
        return 'B'
    elif parte >= 192 and parte <= 223:
        return 'C'
    elif parte >= 224 and parte <= 239:
        return 'D'
    elif parte >= 240 and parte <= 254:
        return 'E'
    else:
        return 'Invalid IP'
def broadcast(ip):
    broadcast=ipaddress.ip_network(ip, strict=False)
    return (str)(broadcast)

def netid(ip):
    netid=ipaddress.ip_network(ip, strict=True)
    return (str)(netid)

    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print('Connected by', addr)
    ip=conn.recv(1024)
    print('IP client: %s'% ip.decode('utf-8'))
    print('Classe IP: %s'% ip_class(ip.decode('utf-8')))
    print('Broadcast: %s'% broadcast(ip.decode('utf-8')))
    print('Netid: %s'% netid(ip.decode('utf-8')))
    


    # socket must be closed by client! sleep for 1 second to wait for the client
    time.sleep(1)
    # otherwise socket goes to TIME_WAIT!
