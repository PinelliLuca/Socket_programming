import sys
import json
import socket

def is_valid_cidr(cidr):
    # Verifica se il formato del CIDR è valido
    parts = cidr.split('/')
    if len(parts) != 2:
        return False
    ip, mask = parts
    if not ip or not mask:
        return False
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py <CIDR>")
        return
    
    cidr = sys.argv[1]
    if not is_valid_cidr(cidr):
        print("Invalid CIDR format")
        return
    
    ip, mask = cidr.split('/')
    
    data = {
        "netid": ip,
        "netmaskCIDR": mask
    }
    
    data_json = json.dumps(data)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('127.0.0.1', 8080))
        
        # Invio dei dati JSON al server
        client_socket.sendall(data_json.encode())
        
        # Ricezione della risposta dal server
        response = client_socket.recv(1024).decode()
        response_data = json.loads(response)
        
        if response_data.get("status") == "OK":
            print("IP Minimo:", response_data["IPmin"])
            print("IP Massimo:", response_data["IPmax"])
        elif response_data.get("status") == "ERROR":
            print("Errore: Dati errati inviati al server")

if __name__ == "__main__":
    main()
