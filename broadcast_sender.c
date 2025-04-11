#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <ifaddrs.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#ifdef _WIN32
#include <winsock2.h>
#include <iphlpapi.h>
#include <windows.h>
#endif

void send_broadcast_message(struct in_addr broadcast_addr) {
    int sockfd;
    char *message = "Message de test en broadcast";

    // Création du socket UDP
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Erreur lors de la création du socket");
        exit(EXIT_FAILURE);
    }

    // Permettre l'envoi en broadcast
    int broadcast_permission = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, (char *)&broadcast_permission, sizeof(broadcast_permission)) < 0) {
        perror("Erreur lors de la définition de l'option de broadcast");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Configurer l'adresse de broadcast
    struct sockaddr_in broadcast_addr_struct;
    memset(&broadcast_addr_struct, 0, sizeof(broadcast_addr_struct));
    broadcast_addr_struct.sin_family = AF_INET;
    broadcast_addr_struct.sin_port = htons(5000);  // Choisir un port pour l'envoi
    broadcast_addr_struct.sin_addr = broadcast_addr;  // Adresse de broadcast

    // Envoi du message
    if (sendto(sockfd, message, strlen(message), 0, (struct sockaddr *)&broadcast_addr_struct, sizeof(broadcast_addr_struct)) < 0) {
        perror("Erreur lors de l'envoi du message");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("Message envoyé en broadcast à %s\n", inet_ntoa(broadcast_addr));

    close(sockfd);
}

#ifdef _WIN32
void get_interfaces_and_calculate_broadcast_windows() {
    DWORD dwSize = 0;
    DWORD dwRetVal = 0;
    IP_ADAPTER_INFO *pAdapterInfo, *pAdapter;
    pAdapterInfo = (IP_ADAPTER_INFO *)malloc(sizeof(IP_ADAPTER_INFO));
    if (pAdapterInfo == NULL) {
        printf("Erreur d'allocation mémoire\n");
        return;
    }

    // Récupérer les informations des adaptateurs
    dwRetVal = GetAdaptersInfo(pAdapterInfo, &dwSize);
    if (dwRetVal == ERROR_BUFFER_OVERFLOW) {
        pAdapterInfo = (IP_ADAPTER_INFO *)realloc(pAdapterInfo, dwSize);
        dwRetVal = GetAdaptersInfo(pAdapterInfo, &dwSize);
    }

    if (dwRetVal != ERROR_SUCCESS) {
        printf("Erreur lors de la récupération des informations des adaptateurs\n");
        free(pAdapterInfo);
        return;
    }

    // Parcours des interfaces
    for (pAdapter = pAdapterInfo; pAdapter != NULL; pAdapter = pAdapter->Next) {
        if (strcmp(pAdapter->AdapterName, "lo") == 0) // Ignorer 'lo' (localhost)
            continue;

        struct in_addr addr, mask, network, broadcast;
        char ip_buffer[16];
        char mask_buffer[16];
        char broadcast_buffer[16];

        // Adresse IP
        inet_pton(AF_INET, pAdapter->IpAddressList.IpAddress.String, &addr);

        // Masque de sous-réseau
        inet_pton(AF_INET, pAdapter->IpAddressList.IpMask.String, &mask);

        // Calcul de l'adresse réseau
        network.s_addr = addr.s_addr & mask.s_addr;

        // Calcul de l'inverse du masque
        struct in_addr inverse_mask;
        inverse_mask.s_addr = ~mask.s_addr;

        // Calcul de l'adresse de broadcast
        broadcast.s_addr = network.s_addr | inverse_mask.s_addr;

        // Affichage des informations pour chaque interface
        printf("Interface: %s\n", pAdapter->Description);
        printf("Adresse IP: %s\n", pAdapter->IpAddressList.IpAddress.String);
        printf("Masque: %s\n", pAdapter->IpAddressList.IpMask.String);
        printf("Adresse réseau: %s\n", inet_ntoa(network));
        printf("Adresse de broadcast: %s\n\n", inet_ntoa(broadcast));

        // Envoi du message en broadcast
        send_broadcast_message(broadcast);
    }

    free(pAdapterInfo);
}
#else
void get_interfaces_and_calculate_broadcast_linux() {
    struct ifaddrs *ifaddr, *ifa;
    struct sockaddr_in *addr, *mask;

    if (getifaddrs(&ifaddr) == -1) {
        perror("getifaddrs");
        exit(EXIT_FAILURE);
    }

    // Parcours des interfaces pour déterminer leur adresse réseau et de broadcast
    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr == NULL || ifa->ifa_netmask == NULL)
            continue;

        // Exclure l'interface de boucle locale 'lo' (localhost)
        if (strcmp(ifa->ifa_name, "lo") == 0)
            continue;

        if (ifa->ifa_addr->sa_family == AF_INET) {  // Vérifie qu'il s'agit d'une adresse IPv4
            addr = (struct sockaddr_in *)ifa->ifa_addr;
            mask = (struct sockaddr_in *)ifa->ifa_netmask;

            // Calcul de l'adresse réseau
            struct in_addr network;
            network.s_addr = addr->sin_addr.s_addr & mask->sin_addr.s_addr;

            // Calcul de l'inverse du masque
            struct in_addr inverse_mask;
            inverse_mask.s_addr = ~mask->sin_addr.s_addr;

            // Calcul de l'adresse de broadcast
            struct in_addr broadcast;
            broadcast.s_addr = network.s_addr | inverse_mask.s_addr;

            // Affichage des informations pour chaque interface
            printf("Interface: %s\n", ifa->ifa_name);
            printf("Adresse IP: %s\n", inet_ntoa(addr->sin_addr));
            printf("Masque: %s\n", inet_ntoa(mask->sin_addr));
            printf("Adresse réseau: %s\n", inet_ntoa(network));
            printf("Adresse de broadcast: %s\n\n", inet_ntoa(broadcast));

            // Envoi du message en broadcast
            send_broadcast_message(broadcast);
        }
    }

    freeifaddrs(ifaddr);
}
#endif

int main() {
#ifdef _WIN32
    WSADATA wsaData;
    // Initialiser Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("Échec de l'initialisation de Winsock\n");
        return 1;
    }

    get_interfaces_and_calculate_broadcast_windows();

    // Fermer Winsock
    WSACleanup();
#else
    get_interfaces_and_calculate_broadcast_linux();
#endif
    return 0;
}
