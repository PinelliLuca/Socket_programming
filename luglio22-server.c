/* A simple server in the internet domain using TCP
   The port number is passed as an argument */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <ctype.h>

void error(char *msg){
    perror(msg);
    exit(1);
}

char* getLastWord(char* str, const char* token) { //token è la stringa da rimuovere
    char* after_token = strstr(str, token);
    if (after_token == NULL) {
        return NULL; // token not found
    }
    after_token += strlen(token); // salto la stringa token

    return after_token; 
}
int main(int argc, char *argv[]){
     int sockfd, newsockfd, portno, clilen;
     char buffer[256];
     struct sockaddr_in serv_addr, cli_addr;
     int n;
     sockfd = socket(AF_INET, SOCK_STREAM, 0);
     char *last_word;
     if (sockfd < 0) 
        error("ERROR opening socket");
     bzero((char *) &serv_addr, sizeof(serv_addr));
     portno = 8080; //numero porta server
     serv_addr.sin_family = AF_INET;
     serv_addr.sin_addr.s_addr = INADDR_ANY;
     serv_addr.sin_port = htons(portno);
     if (bind(sockfd, (struct sockaddr *) &serv_addr,
              sizeof(serv_addr)) < 0) 
              error("ERROR on binding");
     listen(sockfd,5);
     clilen = sizeof(cli_addr);
     newsockfd = accept(sockfd, 
                 (struct sockaddr *) &cli_addr, 
                 &clilen);
     if (newsockfd < 0) 
          error("ERROR on accept");
     bzero(buffer,256);
     n = read(newsockfd,buffer,255);
     if (n < 0) error("ERROR reading from socket");
     //stampo la stringa ricevuta dal client
     printf("%s\n",buffer);
     //ora lavoro sulla concatenzione della stringa ricevuta dal client con la stringa token_server
     char *token_server="token from server: ";
     last_word = getLastWord(buffer, "token from user: "); //last_word è il messaggio inviato dal client
     //gestisco eccezione
     if(last_word == NULL) {
         printf("token not found\n");
         return 0;
     }
     //modifico la parola trasformandola in uppercase
       for (int i = 0; i < strlen(last_word); i++) {
         last_word[i] = toupper(last_word[i]);
         }
         //concatenazione della stringa token_server con il messaggio
         strncat(token_server,last_word,sizeof(token_server)-strlen(last_word)-1);
         //invio la stringa al client
         n = write(newsockfd,token_server,strlen(token_server));
         if (n < 0) error("ERROR writing to socket");
       
       
     return 0; 
}
