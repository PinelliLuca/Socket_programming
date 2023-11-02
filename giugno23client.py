#!/usr/bin/env python3

import socket
import sys
#import ipaddress
import json


HOST='127.0.0.1'
PORT=8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    msg =sys.argv[1]
    msg = json.dumps(msg)
    s.sendall(msg.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    data = json.loads(data)
    #stampo il primo valore status, indipendentemente da valore. Se è OK stampo anche gli altri due valori
    print(data["status"])
    if(data["status"]=="OK"):
        print(data["IPmin"])
        print(data["IPmax"])
        
    s.close()

