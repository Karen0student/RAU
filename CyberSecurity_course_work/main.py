from scapy.all import IP, TCP, ICMP, wrpcap, sendp, rdpcap, send, Raw
import sys
import re

def generate_packet(Action, Protocol, Source_address, Source_port, Destination_address, Destination_port, message_content,
                            sid_content, rev_content):
    payload = ""
    if message_content:
        payload += f"msg:{message_content} "
    if sid_content:
        payload += f"sid:{int(sid_content)} "
    if rev_content:
        payload += f"rev:{int(rev_content)} "
    
    if Protocol == "tcp":
        tcp_packet = IP(src=str(Source_address), dst=str(Destination_address)) / TCP(dport=int(Destination_port), flags='PA', seq=100, sport=int(Source_port)) / payload
        response = send(tcp_packet, verbose=True)
        print(f"response: {response}")
    return
    
    
def main():
    
    while True:
        wordlist = sys.stdin.readline()
        if wordlist:
            Rule_header = re.split(r'\(.*\)', wordlist)
            Rule_header = Rule_header[0].strip()
            Rule_header = [part.strip() for part in Rule_header.split(' ') if part != '->']

            Action = Rule_header[0]
            Protocol = Rule_header[1]
            Source_address = Rule_header[2]
            Source_port = Rule_header[3]
            Destination_address = Rule_header[4]
            Destination_port = Rule_header[5]
            message_match = re.search(r'msg:"([^"]*)"', wordlist)
            sid_match = re.search(r'\bsid\s*:\s*(\d+)\b', wordlist)
            rev_match = re.search(r'\brev\s*:\s*(\d+)\b', wordlist)
            # If message_content is found, extract it; otherwise, set message_content to None
            try:
                message_content = message_match.group(1)
            except AttributeError:
                message_content = None
                
            # If sid_content is found, extract it; otherwise, set sid_content to None
            try:
                sid_content = sid_match.group(1)
            except AttributeError:
                sid_content = None
            
            # If rev_content is found, extract it; otherwise, set rev_content to None
            try:
                rev_content = rev_match.group(1)
            except AttributeError:
                rev_content = None
            
            generate_packet(Action, Protocol, Source_address, Source_port, Destination_address, Destination_port, message_content,
                            sid_content, rev_content)
        else:
            break

    
main()