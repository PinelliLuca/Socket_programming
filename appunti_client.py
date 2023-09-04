#!/usr/bin/env python3

import socket
import sys
import time

#controllo numero di parametri corretto
if len(sys.argv) != 2:
        print("Usage: python client.py <CIDR>")
        return

#suddividere qualcosa in pezzi
data1,data2= qualcosa.split('/')

#valori multipli tipo da usare in json
data = {
        "netid": ip,
        "netmaskCIDR": mask
    }

#invio dati con JSON
#comprimo dati in JSON
data_json = json.dumps(data)
#nel with invio con sendall e codifico i dati
client_socket.sendall(data_json.encode())

#ricezione dati con JSON
#prima ricevo i dati dal server e decodifico
response = client_socket.recv(1024).decode()
#decodifico dati in formato JSON
        response_data = json.loads(response)

#eseguo dopo aver controllato lo status inviatomi dal server
if response_data.get("status") == "OK":
        print()