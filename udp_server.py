import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 12345

# Création du socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Serveur en attente sur {UDP_IP}:{UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)  # Réception du message
    print(f"Message reçu de {addr}: {data.decode()}")
