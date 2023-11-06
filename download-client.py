import socket
import json

# Configura il client
server_host = 'localhost'
server_port = 8080

# Crea un socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((server_host, server_port))

    # Crea una richiesta JSON
    richiesta = {
        "filename": "file.txt"
    }

    # Invia la richiesta JSON al server
    s.send(json.dumps(richiesta).encode('utf-8'))

    # Ricevi la risposta JSON dal server
    risposta_json = s.recv(1024).decode('utf-8')
    risposta = json.loads(risposta_json)

    if 'errore' in risposta:
        print(f"Errore: {risposta['errore']}")
    else:
        nome_file = risposta['filename']
        dimensione_file = int(risposta['filesize'])

        # Ricevi il contenuto del file dal server in un unico blocco
        contenuto_file = s.recv(dimensione_file)

        with open(nome_file, 'wb') as file:
            file.write(contenuto_file)

        print(f"File '{nome_file}' scaricato con successo.")

# Il socket viene chiuso automaticamente alla fine del blocco 'with'
