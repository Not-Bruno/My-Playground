import socket
import tkinter as tk

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

    # GUI
    root = tk.Tk()
    root.title("Signal Empfänger")

    # Textfeld
    text = tk.Text(root, wrap='word')
    text.pack(fill='both', expand=True)

    while True:
        # Empfange Informationen zum Betriebssystem und angemeldeten Benutzer
        system_user = client_socket.recv(1024).decode()
        text.insert('insert', f"{system_user}\n")

        # Empfange Signale
        signal = client_socket.recv(1024).decode()
        if signal:
            text.insert('insert', f"Signal empfangen: {signal}\n")
        else:
            break

    # GUI-Loop
    root.mainloop()

    # Schließe die Verbindung
    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    receive_signals()