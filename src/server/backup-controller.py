import socket
import struct

def packet_to_string(packet):
    eth_header = packet[:14]
    eth = struct.unpack('!6s6sH', eth_header)
    eth_protocol = socket.ntohs(eth[2])
    
    if eth_protocol == 8:
        ip_header = packet[14:34]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8])
        d_addr = socket.inet_ntoa(iph[9])
        return f"Protocol: {protocol}, Source Address: {s_addr}, Destination Address: {d_addr}"
    else:
        return ""

def main():
    with open('network_traffic.log', 'w') as f:
        conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.ntohs(3))
        while True:
            packet, _ = conn.recvfrom(65535)
            log = packet_to_string(packet)
            if log:
                print(log)
                f.write(log + '\n')

if __name__ == '__main__':
    main()

