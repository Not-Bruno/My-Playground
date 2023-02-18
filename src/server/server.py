import socket
import json
import sqlite3
import configparser
import os
from PIL import Image

if __name__ == '__main__':
    # Definition des Base Pfades
    base_path = os.path.abspath(os.path.dirname(__file__))
    # Icon-Image laden
    image = Image.open(os.path.join(base_path, 'content', 'app_ico.png'))
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agent_config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)

    # Host und Port, auf dem der Socket-Server lauscht
    HOST = config.get("NETWORK", "server_addr")
    PORT = config.getint("NETWORK", "server_port")

    # Datenbank-Verbindung herstellen
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    # Eine Funktion, um empfangene Daten in die Datenbank einzufügen
    def insert_data(data):
        c.execute("INSERT INTO cpu_data (cpu_percent, cpu_count) VALUES (?, ?)", (data["cpu_percent"], data["cpu_count"]))
        conn.commit()

    # Socket-Server verbinden und Daten empfangen
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            # Daten empfangen und in die Datenbank einfügen
            data = s.recv(1024)
            client_data = json.loads(data.decode())
            insert_data(client_data)