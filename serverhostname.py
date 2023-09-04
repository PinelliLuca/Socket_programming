#!/usr/bin/env python3

import socket
import sys
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 2525

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    client_socket, client_address = s.accept()
    #print(f"Server connesso alla porta {PORT}")
    data = client_socket.recv(1024)
    print("Client hostname is: %s" % data.decode("utf-8"))
    
    # socket must be closed by client! sleep for 1 second to wait for the client
    time.sleep(1)
    # otherwise socket goes to TIME_WAIT!
