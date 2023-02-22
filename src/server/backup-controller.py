import pcapy

def print_packet(packet):
    print(f"Received a packet: {packet}")

devs = pcapy.findalldevs()
print(f"Available devices: {devs}")

# Öffne das erste Interface
cap = pcapy.open_live(devs[0], 65536, True, 100)

# Setze den Filter auf eingehende Pakete
cap.setfilter('inbound')

# Schleife, um eingehende Pakete zu verarbeiten
while True:
    (header, packet) = cap.next()
    if packet:
        print_packet(packet)
