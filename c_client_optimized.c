#ifdef _WIN32
#define _WIN32_WINNT 0x0600
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>
#include <windows.h>
#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "iphlpapi.lib")
#define bzero(b, len) memset((b), 0, (len))
#else
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <netinet/in.h>
#include <netinet/udp.h>
#include <netdb.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <ifaddrs.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define BUF_SIZE 1024
#define BROADCAST_PORT 5002
#define LISTEN_PORT 5001
#define PYTHON_PORT 5000
#define MESSAGE_ID_LEN 16

char instance_id[MESSAGE_ID_LEN + 1];

void generate_instance_id()
{
    srand((unsigned int)time(NULL));
    for (int i = 0; i < MESSAGE_ID_LEN; i++)
    {
        int r = rand() % 36;
        instance_id[i] = r < 10 ? '0' + r : 'A' + (r - 10);
    }
    instance_id[MESSAGE_ID_LEN] = '\0';
}

void print_timestamp()
{
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    printf("[%02d:%02d:%02d] ", t->tm_hour, t->tm_min, t->tm_sec);
}

void error(const char *msg)
{
    print_timestamp();
    perror(msg);
    exit(1);
}

int verify_package(char *pack)
{
    return 1;
}

int is_own_message(char *message)
{
    char id_prefix[MESSAGE_ID_LEN + 2];
    snprintf(id_prefix, sizeof(id_prefix), "%s|", instance_id);
    return (strncmp(message, id_prefix, strlen(id_prefix)) == 0);
}

void extract_message(char *marked_message, char *extracted_message, int max_len)
{
    char *separator = strchr(marked_message, '|');
    if (separator)
    {
        strncpy(extracted_message, separator + 1, max_len - 1);
    }
    else
    {
        strncpy(extracted_message, marked_message, max_len - 1);
    }
    extracted_message[max_len - 1] = '\0';
}

void send_broadcast_message(struct in_addr broadcast_addr, char *message, int message_len)
{
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0)
        error("Erreur création socket");

    int broadcast_permission = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, (char *)&broadcast_permission, sizeof(broadcast_permission)) < 0)
        error("Erreur option broadcast");

    int reuse = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, (char *)&reuse, sizeof(reuse)) < 0)
        error("Erreur option SO_REUSEADDR");

#ifdef SO_REUSEPORT
    int reuse_port = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEPORT, (char *)&reuse_port, sizeof(reuse_port)) < 0)
        error("Erreur option SO_REUSEPORT");
#endif

    struct sockaddr_in broadcast_addr_struct = {
        .sin_family = AF_INET,
        .sin_port = htons(BROADCAST_PORT),
        .sin_addr = broadcast_addr};

    char marked_message[BUF_SIZE];
    snprintf(marked_message, BUF_SIZE, "%s|%s", instance_id, message);
    int marked_message_len = strlen(marked_message) + 1;

    char addr_str[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &broadcast_addr, addr_str, INET_ADDRSTRLEN);
    print_timestamp();
    printf("ENVOI BROADCAST: Adresse %s, Port %d, Message: %s\n",
           addr_str, BROADCAST_PORT, marked_message);

    if (sendto(sockfd, marked_message, marked_message_len, 0,
               (struct sockaddr *)&broadcast_addr_struct, sizeof(broadcast_addr_struct)) < 0)
        error("Erreur envoi message");

#ifdef _WIN32
    closesocket(sockfd);
#else
    close(sockfd);
#endif
}

#ifdef _WIN32
void broadcast_interfaces_windows(char *message, int message_len)
{
    print_timestamp();
    printf("DÉBUT DIFFUSION: Envoi du message '%s' sur toutes les interfaces Windows\n", message);

    PIP_ADAPTER_INFO pAdapterInfo = NULL;
    ULONG ulOutBufLen = sizeof(IP_ADAPTER_INFO);

    if (GetAdaptersInfo(pAdapterInfo, &ulOutBufLen) == ERROR_BUFFER_OVERFLOW)
    {
        pAdapterInfo = (IP_ADAPTER_INFO *)malloc(ulOutBufLen);
        if (!pAdapterInfo)
            error("Allocation mémoire");
    }

    if (GetAdaptersInfo(pAdapterInfo, &ulOutBufLen) != ERROR_SUCCESS)
        error("Récupération interfaces");

    int count = 0;
    for (PIP_ADAPTER_INFO pAdapter = pAdapterInfo; pAdapter; pAdapter = pAdapter->Next)
    {
        if (pAdapter->Type == MIB_IF_TYPE_LOOPBACK)
            continue;

        struct in_addr addr, mask, broadcast;
        inet_pton(AF_INET, pAdapter->IpAddressList.IpAddress.String, &addr);
        inet_pton(AF_INET, pAdapter->IpAddressList.IpMask.String, &mask);

        broadcast.s_addr = (addr.s_addr & mask.s_addr) | ~mask.s_addr;

        char addr_str[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &broadcast, addr_str, INET_ADDRSTRLEN);
        // print_timestamp();
        // printf("INTERFACE %d: Diffusion sur %s (%s)\n", ++count, pAdapter->Description, addr_str);

        send_broadcast_message(broadcast, message, message_len);
    }

    print_timestamp();
    printf("FIN DIFFUSION: Message envoyé sur %d interfaces\n", count);
    free(pAdapterInfo);
}
#else
void broadcast_interfaces_linux(char *message, int message_len)
{
    print_timestamp();
    printf("DÉBUT DIFFUSION: Envoi du message '%s' sur toutes les interfaces Linux\n", message);

    struct ifaddrs *ifaddr;
    if (getifaddrs(&ifaddr) == -1)
        error("Erreur lors de la récupération interfaces");

    int count = 0;
    for (struct ifaddrs *ifa = ifaddr; ifa; ifa = ifa->ifa_next)
    {
        if (!ifa->ifa_addr || ifa->ifa_addr->sa_family != AF_INET)
            continue;
        if (strcmp(ifa->ifa_name, "lo") == 0)
            continue;

        struct sockaddr_in *addr = (struct sockaddr_in *)ifa->ifa_addr;
        struct sockaddr_in *mask = (struct sockaddr_in *)ifa->ifa_netmask;

        struct in_addr broadcast;
        broadcast.s_addr = (addr->sin_addr.s_addr & mask->sin_addr.s_addr) | ~mask->sin_addr.s_addr;

        char addr_str[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &broadcast, addr_str, INET_ADDRSTRLEN);
        // print_timestamp();
        // printf("INTERFACE %d: Diffusion sur %s (%s)\n", ++count, ifa->ifa_name, addr_str);

        send_broadcast_message(broadcast, message, message_len);
    }

    // print_timestamp();
    // printf("FIN DIFFUSION: Message envoyé sur %d interfaces\n", count);
    freeifaddrs(ifaddr);
}
#endif

#ifdef _WIN32
int is_local_address(struct in_addr addr)
{
    if ((addr.s_addr & htonl(0xFF000000)) == htonl(0x7F000000))
        return 1;

    PIP_ADAPTER_INFO pAdapterInfo = NULL;
    ULONG ulOutBufLen = sizeof(IP_ADAPTER_INFO);
    pAdapterInfo = (IP_ADAPTER_INFO *)malloc(ulOutBufLen);

    if (GetAdaptersInfo(pAdapterInfo, &ulOutBufLen) == ERROR_BUFFER_OVERFLOW)
    {
        free(pAdapterInfo);
        pAdapterInfo = (IP_ADAPTER_INFO *)malloc(ulOutBufLen);
    }

    if (GetAdaptersInfo(pAdapterInfo, &ulOutBufLen) == NO_ERROR)
    {
        for (PIP_ADAPTER_INFO pAdapter = pAdapterInfo; pAdapter; pAdapter = pAdapter->Next)
        {
            for (PIP_ADDR_STRING pAddr = &pAdapter->IpAddressList; pAddr; pAddr = pAddr->Next)
            {
                struct in_addr local_addr;
                inet_pton(AF_INET, pAddr->IpAddress.String, &local_addr);
                if (local_addr.s_addr == addr.s_addr)
                {
                    free(pAdapterInfo);
                    return 1;
                }
            }
        }
    }

    free(pAdapterInfo);
    return 0;
}
#else
int is_local_address(struct in_addr addr)
{
    if ((addr.s_addr & htonl(0xFF000000)) == htonl(0x7F000000))
        return 1;

    struct ifaddrs *ifaddr, *ifa;
    int result = 0;

    if (getifaddrs(&ifaddr) == -1)
        return 0;

    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next)
    {
        if (!ifa->ifa_addr)
            continue;
        if (ifa->ifa_addr->sa_family == AF_INET)
        {
            struct sockaddr_in *local_addr = (struct sockaddr_in *)ifa->ifa_addr;
            if (local_addr->sin_addr.s_addr == addr.s_addr)
            {
                result = 1;
                break;
            }
        }
    }

    freeifaddrs(ifaddr);
    return result;
}
#endif

int main()
{
#ifdef _WIN32
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
        error("Erreur d'initialisation Winsock");
#endif

    generate_instance_id();
    print_timestamp();
    printf("IDENTIFIANT UNIQUE: %s\n", instance_id);

    int python_sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (python_sock < 0)
        error("Création socket pour Python");

    int reuse = 1;
    if (setsockopt(python_sock, SOL_SOCKET, SO_REUSEADDR, (char *)&reuse, sizeof(reuse)) < 0)
        error("Erreur option SO_REUSEADDR pour socket Python");

#ifdef SO_REUSEPORT
    int reuse_port = 1;
    if (setsockopt(python_sock, SOL_SOCKET, SO_REUSEPORT, (char *)&reuse_port, sizeof(reuse_port)) < 0)
        error("Erreur option SO_REUSEPORT pour socket Python");
#endif

    struct sockaddr_in python_recv_addr = {
        .sin_family = AF_INET,
        .sin_port = htons(LISTEN_PORT),
        .sin_addr.s_addr = INADDR_ANY};

    if (bind(python_sock, (struct sockaddr *)&python_recv_addr, sizeof(python_recv_addr)) < 0)
        error("Bind socket Python");

    int broadcast_sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (broadcast_sock < 0)
        error("Création socket pour broadcast");

    if (setsockopt(broadcast_sock, SOL_SOCKET, SO_REUSEADDR, (char *)&reuse, sizeof(reuse)) < 0)
        error("Erreur option SO_REUSEADDR pour socket broadcast");

#ifdef SO_REUSEPORT
    if (setsockopt(broadcast_sock, SOL_SOCKET, SO_REUSEPORT, (char *)&reuse_port, sizeof(reuse_port)) < 0)
        error("Erreur option SO_REUSEPORT pour socket broadcast");
#endif

    struct sockaddr_in broadcast_recv_addr = {
        .sin_family = AF_INET,
        .sin_port = htons(BROADCAST_PORT),
        .sin_addr.s_addr = INADDR_ANY};

    if (bind(broadcast_sock, (struct sockaddr *)&broadcast_recv_addr, sizeof(broadcast_recv_addr)) < 0)
        error("Bind socket broadcast");

    print_timestamp();
    printf("===============================================\n");
    printf("     DÉMARRAGE SERVEUR UDP BIDIRECTIONNEL     \n");
    printf("===============================================\n");
    print_timestamp();
    printf("- Écoute Python sur port %d\n", LISTEN_PORT);
    print_timestamp();
    printf("- Écoute broadcast sur port %d\n", BROADCAST_PORT);
    print_timestamp();
    printf("- SO_REUSEADDR activé sur les deux sockets\n");
#ifdef SO_REUSEPORT
    print_timestamp();
    printf("- SO_REUSEPORT activé sur les deux sockets\n");
#endif
    print_timestamp();
    printf("-----------------------------------------------\n");

    fd_set readfds;
    int max_fd = (python_sock > broadcast_sock) ? python_sock : broadcast_sock;

    while (1)
    {
        FD_ZERO(&readfds);
        FD_SET(python_sock, &readfds);
        FD_SET(broadcast_sock, &readfds);

        if (select(max_fd + 1, &readfds, NULL, NULL, NULL) < 0)
            error("Erreur select");

        if (FD_ISSET(python_sock, &readfds))
        {
            char message[BUF_SIZE + 1];
            struct sockaddr_in client_addr;
            socklen_t addr_len = sizeof(client_addr);

            int received = recvfrom(python_sock, message, BUF_SIZE, 0,
                                    (struct sockaddr *)&client_addr, &addr_len);

            if (received < 0)
            {
                error("Réception message Python");
            }
            else if (received > 0)
            {
                message[received] = '\0';
                print_timestamp();
                printf("REÇU PYTHON: De %s:%d - Message: '%s'\n",
                       inet_ntoa(client_addr.sin_addr),
                       ntohs(client_addr.sin_port), message);

                if (verify_package(message))
                {
                    print_timestamp();
                    printf("DIFFUSION: Message de Python vers broadcast: '%s'\n", message);
#ifdef _WIN32
                    broadcast_interfaces_windows(message, received);
#else
                    broadcast_interfaces_linux(message, received);
#endif
                }
                else
                {
                    print_timestamp();
                    printf("ERREUR PACKAGE: Message non valide, diffusion ignorée\n");
                }
            }
        }

        if (FD_ISSET(broadcast_sock, &readfds))
        {
            char marked_message[BUF_SIZE + 1];
            struct sockaddr_in client_addr;
            socklen_t addr_len = sizeof(client_addr);

            int received = recvfrom(broadcast_sock, marked_message, BUF_SIZE, 0,
                                    (struct sockaddr *)&client_addr, &addr_len);

            if (received < 0)
            {
                error("Réception message broadcast");
            }
            else if (received > 0)
            {
                marked_message[received] = '\0';
                print_timestamp();
                printf("REÇU BROADCAST: De %s:%d - Message: '%s'\n",
                       inet_ntoa(client_addr.sin_addr),
                       ntohs(client_addr.sin_port), marked_message);

                if (is_local_address(client_addr.sin_addr) || is_own_message(marked_message))
                {
                    // print_timestamp();
                    // if (is_local_address(client_addr.sin_addr))
                    //     printf("IGNORÉ: Message provenant d'une adresse locale\n");
                    // if (is_own_message(marked_message))
                    //     printf("IGNORÉ: Message contenant notre identifiant\n");
                }
                else
                {
                    char extracted_message[BUF_SIZE];
                    extract_message(marked_message, extracted_message, BUF_SIZE);

                    print_timestamp();
                    printf("ENVOI À PYTHON: Transmission du message: '%s'\n", extracted_message);

                    int sock_python = socket(AF_INET, SOCK_DGRAM, 0);
                    if (sock_python < 0)
                        error("Erreur lors de la création du socket Python");

                    if (setsockopt(sock_python, SOL_SOCKET, SO_REUSEADDR, (char *)&reuse, sizeof(reuse)) < 0)
                        error("Erreur option SO_REUSEADDR pour socket Python temporaire");

#ifdef SO_REUSEPORT
                    if (setsockopt(sock_python, SOL_SOCKET, SO_REUSEPORT, (char *)&reuse_port, sizeof(reuse_port)) < 0)
                        error("Erreur option SO_REUSEPORT pour socket Python temporaire");
#endif

                    struct sockaddr_in python_send_addr = {
                        .sin_family = AF_INET,
                        .sin_addr.s_addr = inet_addr("127.0.0.1"),
                        .sin_port = htons(PYTHON_PORT)};

                    if (sendto(sock_python, extracted_message, strlen(extracted_message), 0,
                               (struct sockaddr *)&python_send_addr, sizeof(python_send_addr)) < 0)
                    {
                        error("Erreur lors de l'envoi au processus Python");
                    }
                    else
                    {
                        print_timestamp();
                        printf("CONFIRMATION: Message envoyé avec succès à 127.0.0.1:%d\n", LISTEN_PORT);
                    }

#ifdef _WIN32
                    closesocket(sock_python);
#else
                    close(sock_python);
#endif
                }
            }
        }
    }

#ifdef _WIN32
    closesocket(python_sock);
    closesocket(broadcast_sock);
    WSACleanup();
#else
    close(python_sock);
    close(broadcast_sock);
#endif
    return 0;
}
