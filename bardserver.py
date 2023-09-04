import socket
import json

def main():
    # Crea il socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind al socket
    server_addr = ("127.0.0.1", 8000)
    sock.bind(server_addr)

    # Ascolta connessioni
    sock.listen(1)

    # Accetta una connessione
    connection, client_addr = sock.accept()

    # Riceve la richiesta dal client
    request = connection.recv(1024).decode()

    # Interpreta la richiesta
    response_data = json.loads(request)

    # Calcola l'indirizzo IP minimo e massimo della sottorete
    ip_address = response_data["netid"]
    netmask_len = int(response_data["netmaskCIDR"])
    ip_min = ip_address & (2**(32 - netmask_len) - 1)
    ip_max = ip_min + (2**netmask_len - 2)

    # Invia la risposta al client
    response = json.dumps({"status": "OK", "IPmin": ip_min, "IPmax": ip_max})
    connection.sendall(response.encode())

    # Chiude la connessione
    connection.close()


if __name__ == "__main__":
    main()