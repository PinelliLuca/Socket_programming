import socket
import json
import ipaddress

def get_min_max_ips(netid, netmaskCIDR):
    # Calcola l'IP minimo e massimo escludendo indirizzi di rete e broadcast
    network = ipaddress.IPv4Network(f'{netid}/{netmaskCIDR}', strict=False)
    ip_min = network.network_address + 1
    ip_max = network.broadcast_address - 1
    return str(ip_min), str(ip_max)

def main():
    HOST = '127.0.0.1'
    PORT = 8080
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        
        print("Server in ascolto su", HOST, "porta", PORT)
        
        while True:
            client_socket, client_address = server_socket.accept()
            print("Connessione accettata da", client_address)
            
            data = client_socket.recv(1024).decode()
            data_json = json.loads(data)
            
            netid = data_json.get("netid")
            netmaskCIDR = data_json.get("netmaskCIDR")
            
            if not netid or not netmaskCIDR:
                response_data = {"status": "ERROR"}
            else:
                ip_min, ip_max = get_min_max_ips(netid, netmaskCIDR)
                response_data = {
                    "status": "OK",
                    "IPmin": ip_min,
                    "IPmax": ip_max
                }
            
            response_json = json.dumps(response_data)
            client_socket.sendall(response_json.encode())
            
            print("Connessione chiusa con", client_address)
            client_socket.close()

if __name__ == "__main__":
    main()
