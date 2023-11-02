#!/usr/bin/env python3

import socket
import sys

HOST='127.0.0.1'
PORT=8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    msg = '1,5'
    s.sendall(msg.encode('utf-8'))
    data = s.recv(1024)
    s.close()

print('Received: %s'% data.decode('utf-8'))