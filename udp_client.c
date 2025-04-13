#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

#define SERVER_IP "127.0.0.1"  // Adresse du serveur Python
#define SERVER_PORT 12345      // Même port que le serveur Python
#define MESSAGE "Hello depuis C !"

int main() {
    int sockfd;
    struct sockaddr_in server_addr;
    
    // 1️⃣ Création du socket UDP
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Erreur lors de la création du socket");
        exit(EXIT_FAILURE);
    }

    // 2️⃣ Configuration de l'adresse du serveur Python
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

    // 3️⃣ Envoi du message
    ssize_t sent_bytes = sendto(sockfd, MESSAGE, strlen(MESSAGE), 0,
                                (struct sockaddr*)&server_addr, sizeof(server_addr));

    if (sent_bytes < 0) {
        perror("Erreur lors de l'envoi du message");
    } else {
        printf("Message envoyé : %s\n", MESSAGE);
    }

    // 4️⃣ Fermeture du socket
    close(sockfd);
    return 0;
}
