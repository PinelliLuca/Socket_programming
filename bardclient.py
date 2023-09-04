import socket
import json

def main(netid):
    # Crea il socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connessione al server
    server_addr = ("127.0.0.1", 8000)
    sock.connect(server_addr)

    # Invia al server la richiesta
    request = json.dumps({"netid": netid})
    sock.sendall(request.encode())

    # Riceve la risposta dal server
    response = sock.recv(1024).decode()

    # Chiudi il socket
    sock.close()

    # Interpreta la risposta
    response_data = json.loads(response)
    if response_data["status"] == "OK":
        print("IP minimo:", response_data["IPmin"])
        print("IP massimo:", response_data["IPmax"])
    else:
        print("Errore:", response_data["status"])


if __name__ == "__main__":
    netid = input("Inserisci il prefisso di rete: ")
    main(netid)