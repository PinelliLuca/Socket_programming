import socket
import json
import ipaddress
import time

def get_min_max_ips(netid, netmaskCIDR):
    # Calcola l'IP minimo e massimo escludendo indirizzi di rete e broadcast
    network = ipaddress.IPv4Network(f'{netid}/{netmaskCIDR}', strict=True)
    ip_min = network.network_address + 1
    ip_max = network.broadcast_address - 1
    return str(ip_min), str(ip_max)

def main():
    HOST = '127.0.0.1' #localhost
    PORT = 8080 #porta standard se non specificata
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
    
        
        while True:
            client_socket, client_address = server_socket.accept()
            print("Connessione accettata da", client_address)
            
            #ricezione dati in JSON
            #Prima ricevo dati inviati da client, decodifico
            data = client_socket.recv(1024).decode()
            #carico dati formato JSON
            data_json = json.loads(data)
            
            #utilizzo get per assegnare dati da JSON
            netid = data_json.get("netid")
            netmaskCIDR = data_json.get("netmaskCIDR")
            #per messaggio di errore nel caso in cui uno dei due sia vuoto
            if not netid or not netmaskCIDR:
                response_data = {"status": "ERROR"}
            
                
            #per rispondere a client in formato JSON è uguale all'invio di dati da client
            response_json = json.dumps(response_data)
            client_socket.sendall(response_json.encode())
            
            print("Connessione chiusa con", client_address)
            
if __name__ == "__main__":
    main()
