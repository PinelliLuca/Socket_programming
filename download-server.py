import socket
import json

# Funzione per gestire le richieste dei client
def gestisci_richiesta(client_socket):
    try:
        # Ricevi la richiesta JSON dal client
        data = client_socket.recv(1024).decode('utf-8')
        richiesta = json.loads(data)

        if 'filename' in richiesta:
            nome_file = richiesta['filename']

            try:
                with open(nome_file, 'rb') as file:
                    contenuto = file.read()
                    dimensione_file = len(contenuto)

                # Costruisci la risposta JSON
                risposta = {
                    "filename": nome_file,
                    "filesize": str(dimensione_file)
                }

                # Invia la risposta JSON al client
                client_socket.sendall(json.dumps(risposta).encode('utf-8'))

                # Invia il contenuto del file al client in un unico blocco
                client_socket.sendall(contenuto)
            except FileNotFoundError:
                errore = {"errore": "Il file richiesto non esiste"}
                client_socket.sendall(json.dumps(errore).encode('utf-8'))
        else:
            errore = {"errore": "Richiesta JSON non valida"}
            client_socket.sendall(json.dumps(errore).encode('utf-8'))
    except json.JSONDecodeError:
        errore = {"errore": "Richiesta JSON non valida"}
        client_socket.sendall(json.dumps(errore).encode('utf-8'))

# Configura il server
server_host = 'localhost'
server_port = 8080

# Crea un socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((server_host, server_port))
    s.listen(1)  # Massimo 1 connessione in attesa
    print(f"In attesa di connessioni su {server_host}:{server_port}...")
    
    conn, addr = s.accept()  # Accetta una connessione in arrivo
    print(f"Connessione da {addr[0]}:{addr[1]}")
    gestisci_richiesta(conn)
      