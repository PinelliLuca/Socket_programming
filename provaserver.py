import socket
import json
import ipaddress

def handle_client(client_socket):
    data = client_socket.recv(1024).decode()
    try:
        payload = json.loads(data)
        net_id = payload["netid"]
        netmask_cidr = payload["netmaskCIDR"]
        
        network = ipaddress.ip_network(f"{net_id}/{netmask_cidr}", strict=False)
        ip_min = str(network.network_address + 1)
        ip_max = str(network.broadcast_address - 1)
        
        response = {
            "status": "OK",
            "IPmin": ip_min,
            "IPmax": ip_max
        }
    except (ValueError, KeyError, ipaddress.AddressValueError):
        response = {
            "status": "ERROR"
        }
    
    response_data = json.dumps(response).encode()
    client_socket.send(response_data)
    client_socket.close()

def s():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(1)
    print("Server in ascolto su 127.0.0.1:8080")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connessione da {client_address[0]}:{client_address[1]}")
        handle_client(client_socket)

if __name__ == "__main__":
    s()
