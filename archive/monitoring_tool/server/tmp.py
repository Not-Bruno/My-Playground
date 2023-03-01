import socket
import json
import sqlite3
import configparser
import os
import socket
import psutil
import time
from PIL import Image

""" :TODO
- Daten Empfangen
- Daten sortieren und in Datenbank speichern
- Evtl in Prozessen gehanthabt
    - CPU Info -> wird gesendet an Port 8234
    - RAM Info -> wird gesendet an Port 8244
    
"""
base_path = os.path.abspath(os.path.dirname(__file__))
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

db_path = config.get("DATABASE", "db_path")

# Funktion zum Eintragen der Daten in die Datenbank
def insert_into_db(processor, memory, disk, ram):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO data (processor, memory, disk, ram) VALUES (?, ?, ?, ?)", (processor, memory, disk, ram))
    conn.commit()
    conn.close()

# Socket initialisieren
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345
server_socket.bind((host, port))

# Auf eingehende Verbindungen warten
server_socket.listen(5)
print("Server lauscht auf Verbindungen...")

while True:
    # Verbindung annehmen
    client_socket, addr = server_socket.accept()
    print(f"Verbindung von {addr} aufgebaut")

    # Daten senden
    while True:
        processor_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        ram_usage = psutil.virtual_memory().used / (1024.0 ** 3)

        # Daten in die Datenbank eintragen
        insert_into_db(processor_usage, memory_usage, disk_usage, ram_usage)

        # Daten senden
        message = f"CPU-Auslastung: {processor_usage}%\nSpeicher-Auslastung: {memory_usage}%\nDisk-Auslastung: {disk_usage}%\nRAM-Auslastung: {ram_usage:.2f} GB\n"
        client_socket.sendall(message.encode())
        time.sleep(1)
        
    # Verbindung schließen
    client_socket.close()