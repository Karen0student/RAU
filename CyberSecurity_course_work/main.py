from scapy.all import IP, TCP, ICMP, UDP, sr1
import sys
import re

def generate_packet(Action, Protocol, Source_address, Source_port, Destination_address, Destination_port, message_content,
                            sid_content, rev_content, http_method, http_client_body, http_uri):
    payload = ""
    if message_content:
        payload += f"msg:{message_content} "
    if sid_content:
        payload += f"sid:{int(sid_content)} "
    if rev_content:
        payload += f"rev:{int(rev_content)} "

    if Protocol == "tcp":
        packet = IP(src=str(Source_address), dst=str(Destination_address)) / TCP(dport=int(Destination_port), flags='S', seq=100, 
                                                                                    sport=int(Source_port)) / payload
    elif Protocol == "icmp":
        packet = IP(src=str(Source_address), dst=str(Destination_address)) / ICMP()
    
    elif Protocol == "udp":
        packet = IP(src=str(Source_address), dst=str(Destination_address)) / UDP(dport=int(Destination_port), 
                                                                                    sport=int(Source_port)) / payload
    else:
        print("ERROR: NOT CORRECT PROTOCOL")
        return
    
    #SENDING PACKET
    response = sr1(packet, verbose=True, timeout=2)
    if response:
        print(f"response: {response.summary()}")
    else:
        print("No response")
    
    return
    
    
def main():
    
    while True:
        wordlist = sys.stdin.readline()
        if wordlist:
            Rule_header = re.split(r'\(.*\)', wordlist)
            Rule_header = Rule_header[0].strip()
            Rule_header = [part.strip() for part in Rule_header.split(' ') if part != '->']
            Action = str(Rule_header[0])
            Protocol = str(Rule_header[1])
            Source_address = str(Rule_header[2])
            Source_port = int(Rule_header[3])
            Destination_address = str(Rule_header[4])
            Destination_port = int(Rule_header[5])
            
            message_match = re.search(r'msg:"([^"]*)"', wordlist)
            sid_match = re.search(r'\bsid\s*:\s*(\d+)\b', wordlist)
            rev_match = re.search(r'\brev\s*:\s*(\d+)\b', wordlist)
            http_method_match = re.search(r'http_method', wordlist)
            http_client_body_match = re.search(r'http_client_body', wordlist)
            http_header_match = re.search(r'http_header', wordlist)
            http_uri_match = re.search(r'http_uri', wordlist)

            try:
                message_content = message_match.group(1)
            except AttributeError:
                message_content = None
                
            try:
                sid_content = sid_match.group(1)
            except AttributeError:
                sid_content = None
            
            try:
                rev_content = rev_match.group(1)
            except AttributeError:
                rev_content = None
            
            try:
                http_method = http_method_match.group()
            except AttributeError:
                http_method = None
                
            try:
                http_client_body = http_client_body_match.group()
            except AttributeError:
                http_client_body = None
            
            try:
                http_header = http_header_match.group()
                print(http_header)
            except AttributeError:
                http_header = None
                
            try:
                http_uri = http_uri_match.group()
            except AttributeError:
                http_uri = None

            generate_packet(Action, Protocol, Source_address, Source_port, Destination_address, Destination_port, message_content,
                            sid_content, rev_content, http_method, http_client_body, http_uri)
        else:
            break

    
main()