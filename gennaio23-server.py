#!/usr/bin/env python3

import socket
import sys
import time
#import ipaddress 

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 5000        # Port to listen on (non-privileged ports are > 1023)

#algoritmo rot11 senza le lettere kwxy
def rot11(x):
    alphabet = 'abcefghijlmnopqrstuvz'  # Alfabeto di 22 caratteri
    result = []
    for c in x:
        if c in alphabet:
            result.append(alphabet[(alphabet.index(c) + 11) % 22])
        else:
            result.append(c)
    return "".join(result)



#algoritmo rot13
def rot13(x):
    x=x.lower()
    alpha='abcdefghijklmnopqrstuvwxyz'
    return "".join([alpha[(alpha.index(c)+13)%26] if c in alpha else c for c in x])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
   
    data = conn.recv(1024).decode('utf-8')
    
    inutile,stringa=data.split(':')
    if( not stringa):
        print('nessuna stringa inserita')
        conn.sendall('nessuna stringa inserita'.encode('utf-8'))
    else:
        stringa2=stringa
        rot13_data=rot13(stringa)
        rot11_data=rot11(stringa2)
        token13='token from server rot13= '+rot13_data+ ' token from server rot11= '+rot11_data
        #rispedisco la stringa al client
        conn.sendall(token13.encode('utf-8'))
    # socket must be closed by client! sleep for 1 second to wait for the client
    time.sleep(1)
    # otherwise socket goes to TIME_WAIT!