#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

void error(char *msg)
{
    perror(msg);
    exit(0);
}

void send_http_request(int sockfd, char * pathname, char * hostname){
    char reqbuffer[256];
    int n;
    bzero(reqbuffer,256);
    sprintf(reqbuffer,"GET %s HTTP/1.1\r\nHost: %s\r\n\r\n", 
            pathname, hostname);
    // printf(reqbuffer);
    n = write(sockfd, reqbuffer, strlen(reqbuffer));
    if (n < 0) 
         error("ERROR writing to socket");
}

void read_http_response(int sockfd){
    char respbuffer[256];
    int n;
    bzero(respbuffer,256);
    n = read(sockfd, respbuffer, 255);
    if (n < 0) 
         error("ERROR reading from socket");
    printf("%s\n", respbuffer);  
}

int main(int argc, char *argv[])
{
    int sockfd, portno;
    struct sockaddr_in serv_addr;
    struct hostent *server;
    char *hostname = "localhost";
    char *pathname;

    if (argc < 1) {
       fprintf(stderr,"usage %s URL\n", argv[0]);
       exit(0);
    }
    pathname=argv[1];
    /*defaul HTTP port*/
    portno = 80;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) 
        error("ERROR opening socket");
    server = gethostbyname(hostname);
    if (server == NULL) {
        fprintf(stderr,"ERROR, no such host\n");
        exit(0);
    }
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, 
         (char *)&serv_addr.sin_addr.s_addr,
         server->h_length);
    serv_addr.sin_port = htons(portno);
    if (connect(sockfd, (const struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) 
        error("ERROR connecting");
    send_http_request(sockfd, pathname, hostname);
    read_http_response(sockfd);
    return 0;
}
