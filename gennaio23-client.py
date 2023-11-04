#!/usr/bin/env python3

import socket
import sys

HOST='127.0.0.1' #sys.argv[1]
PORT=5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    input_str = str(sys.argv[1])
    msg='token from client: '+input_str
    s.sendall(msg.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    print('%s'% data)
    s.close()

