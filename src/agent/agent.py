import platform
import psutil
import time
import logging as logger
import configparser
import pystray
from PIL import Image
import threading
from plyer import notification
import os

# TODO
# App Icon  in Taskleiste
# Log funktion fehler schreibt nicht mehr in definierte Log datei
# Übertragung der Daten zum Server
# Vervollständigung der Config Datei

if __name__ == "__main__":
    # Hier beginnt der Hauptcode mit der while-Schleife
    # Definition des Base Pfades
    base_path = os.path.abspath(os.path.dirname(__file__))
    # Icon-Image laden
    image = Image.open(os.path.join(base_path, 'content', 'app_ico.png'))
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agent_config.ini')
    
    config = configparser.ConfigParser()
    config.read(config_path)
    # Lies den Wert einer Einstellung
    tick = config.getint('SETTINGS', 'refresh_time')
    
    def setup_logging(config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        enable_logging = config.get("LOGGING", "enable_file_logging")   
        print(enable_logging + "-"*100)
        log_file = config.get('LOGGING', 'log_file_path')
        
        try:
            open(log_file, 'x')
            print("File created:", log_file)
        except FileExistsError as e:
            print("File already exists:", log_file)

        # Logger-Konfiguration
        log = logger.getLogger(log_file)
        log.setLevel(logger.DEBUG)

        # Handler für die Ausgabe in eine Datei und auf die Konsole
        file_handler = logger.FileHandler(log_file)
        console_handler = logger.StreamHandler()

        # Formatter für den Log-Eintrag
        formatter = logger.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Füge die Handler zum Logger hinzu
        log.addHandler(file_handler)
        log.addHandler(console_handler)

        def log_func(msg, loglevel):
            if enable_logging:
                if loglevel == "INF":
                    log.info(f'{msg}')
                if loglevel == "WARN":
                    log.warning(f"{msg}")
                if loglevel == "ERROR":
                    log.error(f"{msg}")
            else:
                print(msg)  
        return log_func
    log = setup_logging(config_path)


# BGIN WHILE LOOP ----------------------------------------------------------
    while True:
        # Betriebssysteminformationen
        os_name = platform.system()
        os_release = platform.release()
        os_version = platform.version()

        print("-"*50)
        print(f"Betriebssystem: {os_name} {os_release} ({os_version})")


        # Informationen zur Festplatte
        disk_partitions = psutil.disk_partitions()
        total_size = 0
        free_size = 0

        try: 
            for partition in psutil.disk_partitions():
                # Ignoriert CD-ROMs, Netzlaufwerke und nicht zugängliche Laufwerke
                if 'cdrom' in partition.opts or partition.fstype == '':
                    continue

                # Extrahiert den Laufwerksbuchstaben und den Laufwerkspfad
                device = partition.device
                mount_point = partition.mountpoint

                # Gibt die Größe des Laufwerks und die Menge des verfügbaren Speichers aus
                partition_usage = psutil.disk_usage(mount_point)
                print("-"*50)
                print(f"Device: {device}")
                print(f"  Total: {partition_usage.total / (1024.0 ** 3):.2f} GB")
                print(f"  Used: {partition_usage.used / (1024.0 ** 3):.2f} GB")
                print(f"  Free: {partition_usage.free / (1024.0 ** 3):.2f} GB")

                log("Test", loglevel="INF")

        except PermissionError as e:
            log(f"Laufwerkfehler: Permission Error - {e}", loglevel="INF")


        print("-"*50)
        # Informationen zum Arbeitsspeicher
        mem = psutil.virtual_memory()
        total_mem = mem.total
        used_mem = mem.used

        print(f"Installierter Arbeitsspeicher: {total_mem / 2**30:.2f} GB")
        print(f"Verwendeter Arbeitsspeicher: {used_mem / 2**30:.2f} GB")
        print("-"*50)

        # Anzahl der logischen CPU-Kerne
        logical_cores = psutil.cpu_count()
        print("Anzahl der logischen CPU-Kerne:", logical_cores)

        # Anzahl der physischen CPU-Kerne
        physical_cores = psutil.cpu_count(logical=False)
        print("Anzahl der physischen CPU-Kerne:", physical_cores)

        # CPU-Auslastung
        print("CPU-Auslastung: {}%".format(psutil.cpu_percent(interval=1)))
        print("-"*50)

        """
        # Prozessorzeit für jeden Prozess
        for process in psutil.process_iter(['pid', 'name', 'cpu_times']):
            cpu_time = process.info['cpu_times']
            print("{:<20} - Prozessorzeit: user={:.2f}, system={:.2f}".format(process.info['name'], cpu_time.user, cpu_time.system))
        """


        # Netzwerk-Schnittstellen
        net_io_counters = psutil.net_io_counters(pernic=True)
        for interface, data in net_io_counters.items():
            rec = data.bytes_recv
            send = data.bytes_sent
            print(f"Schnittstelle {interface}:")
            print(f"\tBytes empfangen: {rec:.2f}")
            print(f"\tBytes gesendet: {send:.2f}")

        print("-"*50)

        time.sleep(tick)
# ENDE ----------------------------------------------------------------