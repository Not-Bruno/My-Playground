import socket

# Empfangen von Signalen
def receive_signals():
    # Server-Einstellungen
    host = 'localhost'
    port = 5000

    # Erstelle einen TCP/IP-Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Warte auf Verbindung...")

    # Akzeptiere eine einzige Verbindung
    client_socket, address = server_socket.accept()
    print("Verbunden mit", address)

    with open("rec.txt", "w") as file:
        while True:
            # Empfange Informationen zum Betriebssystem und angemeldeten Benutzer
            system_user = client_socket.recv(1024).decode()
            file.write(f"{system_user}\n")

            # Empfange Signale
            signal = client_socket.recv(1024).decode()
            if signal:
                file.write(f"Signal empfangen: {signal}\n")
            else:
                break

    # Schließe die Verbindung
    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    receive_signals()