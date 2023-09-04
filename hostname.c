#include <stdio.h>
#include <unistd.h>       
#include <string.h>
#include <strings.h>
#include <stdlib.h>

void error(char *msg)
{
    perror(msg);
    exit(0);
}

int main(int argc, char *argv[]){
	char buf[256];
	int prompt_len=0, rv;
	bzero(&buf, sizeof(buf));
	strcpy ((char *) &buf, "welcome from ");
	prompt_len=strlen(buf);
	rv = gethostname((char *) (&buf) + prompt_len, sizeof(buf) - prompt_len);
	if (rv!=0){error("ERROR in gethostname");}
	printf("%s\n", buf);
}
