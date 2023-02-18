import platform
import socket
import psutil
import time
import logging as logger
import configparser
import pystray
from PIL import Image
import threading
import os

# TODO
# App Icon  in Taskleiste
# Code bereinigen
# Logfunktion anpassen
# Übertragung der Daten zum Server
# Vervollständigung der Config Datei

if __name__ == "__main__":
    # Definition des Base Pfades
    base_path = os.path.abspath(os.path.dirname(__file__))
    # Icon-Image laden
    image = Image.open(os.path.join(base_path, 'content', 'app_ico.png'))
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agent_config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    # Lies den Wert einer Einstellung
    tick = config.getint('SETTINGS', 'refresh_time')
    cpu_monitoring = config.getboolean('SERVICE', 'enable_cpu_monitoring')
    storage_monitoring = config.getboolean('SERVICE', 'enable_storage_monitoring')
    ram_monitoring = config.getboolean('SERVICE', 'enable_ram_monitoring')
    network_monitoring = config.getboolean('SERVICE', 'enable_network_monitoring')
    # Host und Port, auf dem der Socket-Server lauscht
    HOST = config.get('NETWORK', 'server_addr')
    PORT = config.getint("NETWORK", "server_port")


    def setup_logging(config_path):
        enable_logging = config.getboolean("LOGGING", "enable_file_logging") # <- Hier wird getboolean() statt get() verwendet

        if not enable_logging:
            def log_func(msg, loglevel):
                print(msg)  
                return
        else:
            log_file = config.get('LOGGING', 'log_file_path')
            try:
                open(log_file, 'x')
                print("File created:", log_file)
            except FileExistsError as e:
                pass

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
                if loglevel == "INF":
                    log.info(f'{msg}')
                if loglevel == "WARN":
                    log.warning(f"{msg}")
                if loglevel == "ERROR":
                    log.error(f"{msg}")
                print(msg) 

        return log_func

    log = setup_logging(config_path)


    def check_disk_usage(threshold, conn):
        """Checks the disk usage for each partition and sends a warning if usage exceeds the specified threshold."""
        for partition in psutil.disk_partitions():
            # Ignore CD-ROMs, network drives, and inaccessible drives
            if 'cdrom' in partition.opts or partition.fstype == '':
                continue
            
            # Extract the drive letter and drive path
            device = partition.device
            mount_point = partition.mountpoint

            # Get the disk usage and calculate the percentage of used space
            partition_usage = psutil.disk_usage(mount_point)
            used_percent = partition_usage.percent

            # Send a warning if the disk usage exceeds the specified threshold
            if used_percent > threshold:
                conn.sendall(f"WARNING: Disk usage for drive {device} is at {used_percent}%!".encode())
                log(f"Drive {device} is at {used_percent}%!", "WARN")
                #print(f"WARNING: Disk usage for drive {device} is at {used_percent}%!")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        # Auf eine eingehende Verbindung warten
        conn, addr = s.accept()
        log(f'Verbunden mit {addr}', "INF")
        #conn.sendall(str(cpu_data).encode())

    # BGIN WHILE LOOP ----------------------------------------------------------
        while True:
            computer_name = socket.gethostname()
            print(f"Hostname: {computer_name}")

            # Betriebssysteminformationen
            os_name = platform.system()
            os_release = platform.release()
            os_version = platform.version()

            print("-"*50)
            conn.sendall(f"Betriebssystem: {os_name} {os_release} ({os_version})".encode())
            #print(f"Betriebssystem: {os_name} {os_release} ({os_version})")

            if storage_monitoring:
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
                        conn.sendall(f"Device: {device}".encode())
                        conn.sendall(f"Total: {partition_usage.total / (1024.0 ** 3):.2f} GB".encode())
                        conn.sendall(f"Used: {partition_usage.used / (1024.0 ** 3):.2f} GB".encode())
                        conn.sendall(f"Free: {partition_usage.free / (1024.0 ** 3):.2f} GB".encode())

                        #print(f"Device: {device}")
                        #print(f"  Total: {partition_usage.total / (1024.0 ** 3):.2f} GB")
                        #print(f"  Used: {partition_usage.used / (1024.0 ** 3):.2f} GB")
                        #print(f"  Free: {partition_usage.free / (1024.0 ** 3):.2f} GB")


                except PermissionError as e:
                    log(f"Laufwerkfehler: Permission Error - {e}", loglevel="INF")

                # Überprüft die Kapazität der Festplatten
                print("-" * 50)
                check_disk_usage(config.getint("SETTINGS", "storage_quota_warn_at"), conn)

            print("-"*50)

            if ram_monitoring:
                # Informationen zum Arbeitsspeicher
                mem = psutil.virtual_memory()
                total_mem = mem.total
                used_mem = mem.used

                print(f"Installierter Arbeitsspeicher: {total_mem / 2**30:.2f} GB")
                print(f"Verwendeter Arbeitsspeicher: {used_mem / 2**30:.2f} GB")
                print("-"*50)

            if cpu_monitoring:
                # Anzahl der logischen CPU-Kerne
                logical_cores = psutil.cpu_count()
                print("Anzahl der logischen CPU-Kerne:", logical_cores)

                # Anzahl der physischen CPU-Kerne
                physical_cores = psutil.cpu_count(logical=False)
                print("Anzahl der physischen CPU-Kerne:", physical_cores)

                # CPU-Auslastung
                print("-"*50)
                cpu_usage = psutil.cpu_percent(interval=1)
                warn_cpu_usage = config.getint("SETTINGS", "cpu_quota_warn_at")
                print(f"CPU-Auslastung: {cpu_usage}%")
                if cpu_usage > warn_cpu_usage:
                    log(f"CPU Auslastung ist über {warn_cpu_usage}%", "WARN")
                    print(f"WARNING: CPU Usage over {warn_cpu_usage}%")
                    print("-"*50)

            """
            # Prozessorzeit für jeden Prozess
            for process in psutil.process_iter(['pid', 'name', 'cpu_times']):
                cpu_time = process.info['cpu_times']
                print("{:<20} - Prozessorzeit: user={:.2f}, system={:.2f}".format(process.info['name'], cpu_time.user, cpu_time.system))
            """

            if network_monitoring:
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