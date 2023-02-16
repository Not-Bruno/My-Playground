import platform
import psutil
import time
import logging as log
import configparser
import pystray
from PIL import Image

# Erstelle das Icon-Image
icon = Image.open("./5122213/app_ico.png")
# Erstelle das Tray-Icon
tray_icon = pystray.Icon("name", icon, "Tooltip", on_clicked)
# Füge das Tray-Icon zur Taskleiste hinzu
tray_icon.run()

# Erstelle ein Konfigurations-Parser-Objekt
config = configparser.ConfigParser()

# Lade die Konfigurationsdatei
config.read('./client_config.ini')

# Lies den Wert einer Einstellung
log_file = config.get('system', 'log_file_path')
logging = config.get("logging", "enable_file_logging")

# Ändere den Wert einer Einstellung
config.set('network', 'port', '9090')

print(logging)

if logging:
    try:
        open(log_file, 'x')
        print("File created:", log_file)
    except FileExistsError:
        print("File already exists:", log_file)

    
    # Logger-Konfiguration
    log = logging.getLogger(log_file)
    log.setLevel(logging.DEBUG)

    # Handler für die Ausgabe in eine Datei und auf die Konsole
    file_handler = log.FileHandler('my_log.log')
    console_handler = log.StreamHandler()

    # Formatter für den Log-Eintrag
    formatter = log.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Füge die Handler zum Logger hinzu
    log.addHandler(file_handler)
    log.addHandler(console_handler)

# Schreibe die geänderten Einstellungen zurück in die Konfigurationsdatei
with open('config.ini', 'w') as f:
    config.write(f)

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
    except PermissionError as e:
        print(f"Laufwerkfehler: PermissionError - {e}")


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

    time.sleep(60)