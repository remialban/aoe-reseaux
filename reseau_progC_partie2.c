#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/udp.h>
#include <netdb.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUF_SIZE 1024
#define EXCEPTION_LEN 500

void stop(char* mes){
    perror(mes);
    exit(EXIT_SUCCESS);
}

int verify_package(char* pack){
    return 1;
}


int main(int argc, char** argv)
{
    char message[BUF_SIZE+1];
    int sockfd, taille;
    printf("beginning\n\n");
    
    if((sockfd = socket(AF_INET, SOCK_DGRAM,0) )==-1)
    {
        stop("socket creation");
    }
    struct sockaddr_in addr;
    bzero(&addr, sizeof(addr));
    if (inet_pton(AF_INET,"127.0.0.1",&addr.sin_addr)==-1){
        stop("attribution de l'adresse");
    }

    printf("the first steps did not break it\n\n");


    addr.sin_family = AF_INET;
    addr.sin_port =  htons(5001);
    socklen_t addr_len = sizeof(addr);
    bind(sockfd, (struct sockaddr *) &addr, sizeof(addr));
    printf("the bind worked \n\n");
   //connect(sockfd, (struct sockaddr *) &addr, sizeof(addr));
    printf("The connect worked \n");

        printf("dans la boucle");
        taille = recvfrom(sockfd, message,BUF_SIZE,MSG_PEEK,(struct sockaddr*)&addr,&addr_len);
        printf("received something\n\n");
        if (taille <0){
            stop("\nerreur_recvfrom\n");
        }
        else {
            message[taille] = '\0';
            printf("\nMessage stocké dans message\n");
        }
        message[BUF_SIZE] = '\0';
        printf(" message : %s\n ", message);
        if(verify_package(message)){
            
            printf("le packet est bon !!!");
            ////
            //stuff from step 3
            ////
                ////other stuff from 4 and 5 
            ////

        }
        else {
            printf("ERREUR!!!! Message invalide :\n\n %s \n\n",message);
        }

    


}