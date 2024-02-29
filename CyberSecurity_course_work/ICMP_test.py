from scapy.all import IP, ICMP, wrpcap, sendp, rdpcap, send, Raw


def generate_icmp_packet(src_ip, dst_ip, msg="ICMP Packet", sid=1000001):
    # Create an ICMP Echo Request packet with specified source/destination IP
    icmp_pkt = IP(src=src_ip, dst=dst_ip) / ICMP() / Raw(load=msg) / Raw(load=str(sid))
    # for _ in range(50):
    #     send(icmp_pkt)
    return icmp_pkt


def write_to_pcap(packets, filename):
    wrpcap(filename, packets)

def send_pcap(filename, iface=None):
    packets = rdpcap(filename)  # Read packets from the pcap file
    send(packets, iface=iface, loop=0)  # Send packets

# Example usage
src_ip = "192.168.0.144"
dst_ip = "192.168.122.94"
msg = "This is an ICMP packet"
sid = 1001
icmp_packet = generate_icmp_packet(src_ip, dst_ip, msg, sid)
#packets = [icmp_packet]  # Assuming you have generated multiple packets
write_to_pcap(icmp_packet, "/home/voyager/Visual_Studio/CyberSecurity_course_work/generated_traffic.pcap")
send_pcap("/home/voyager/Visual_Studio/CyberSecurity_course_work/generated_traffic.pcap")

