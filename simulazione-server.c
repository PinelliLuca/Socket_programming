
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define PORT 8080

void conway(int *seed, int n);

int main(int argc, char const *argv[]) {
    int server_fd, new_socket, valread;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};
    char *msg = "ERR";
    
    // Creazione della socket del server
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }
    
    // Impostazione delle opzioni della socket
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    
    // Impostazione dell'indirizzo del server e della porta
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);
    
    // Binding della socket all'indirizzo e alla porta
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
    
    // Mettere il server in ascolto sulla porta
    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }
    
    while (1) {
        // Accettare le connessioni in entrata
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("accept");
            exit(EXIT_FAILURE);
        }
        
        // Creare un processo figlio per gestire la richiesta
        int pid = fork();
        if (pid == 0) {
            // Processo figlio
            
            // Ricevere i dati in input dal client
            valread = read(new_socket, buffer, 1024);
            if (valread < 0) {
                perror("read");
                exit(EXIT_FAILURE);
            }
            
            // Verificare che i dati siano nel formato corretto
            int seed, n;
            if (sscanf(buffer, "%d,%d", &seed, &n) != 2) {
                send(new_socket, msg, strlen(msg), 0);
                close(new_socket);
                exit(EXIT_SUCCESS);
            }
            
            // Eseguire il processo di decadimento audioattivo di Conway
            conway(&seed, n);
            
            // Inviare i risultati al client
            char result[1024];
            sprintf(result, "%d", seed);
            send(new_socket, result, strlen(result), 0);
            
            // Chiudere la connessione con il client e terminare il processo figlio
            close(new_socket);
            exit(EXIT_SUCCESS);
        } else if (pid < 0) {
            perror("fork");
            exit(EXIT_FAILURE);
        }
        
        // Processo padre
        close(new_socket);
    }
    
    return 0;
}

void conway(int *seed, int n) {
    int i, j;
    int prev[80], curr[80], next[80];
    
    // Inizializzazione della prima riga
    for (i = 0; i < 80; i++) {
        prev[i] = 0;
        curr[i] = 0;
        next[i] = 0;
    }
    curr[40] = *seed;
    
    // Esecuzione del processo di decadimento audioattivo di Conway
    for (i = 0; i < n; i++) {
        // Calcolo della riga successiva
        for (j = 1; j < 79; j++) {
            next[j] = prev[j-1] ^ prev[j+1] ^ curr[j] ^ 1;
        }
        
        // Aggiornamento delle righe
        for (j = 0; j < 80; j++) {
            prev[j] = curr[j];
            curr[j] = next[j];
        }
    }
    
    // Salvataggio del risultato
    *seed = curr[40];
}
