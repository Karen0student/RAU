import re
from scapy.all import IP, TCP, ICMP, UDP, wrpcap, sendp, rdpcap, send, Raw, sr1, sniff, sr
import binascii
import sys
import os


icmp_index = 0
tcp_index = 0
udp_index = 0

def folders(flow=""):
    if not os.path.exists("pcaps"):
        os.makedirs("pcaps")
    if not os.path.exists("pcaps/icmp"):
        os.makedirs("pcaps/icmp")
    if not os.path.exists("pcaps/tcp"):
        os.makedirs("pcaps/tcp")
    if not os.path.exists("pcaps/udp"):
        os.makedirs("pcaps/udp")
    
    # tcp folder organized by their flow
    if flow is not None:
        if not os.path.exists(f"pcaps/tcp/{str(flow)}"):
            os.makedirs(f"pcaps/tcp/{str(flow)}")
    else:
        if not os.path.exists(f"pcaps/tcp/undefined_flow"):
            os.makedirs(f"pcaps/tcp/undefined_flow")


def split_and_convert(text):
    segments = []
    parts = text.split("|")
    for part in parts:
        if all(c in '0123456789abcdefABCDEF ' for c in part):
            # Handle hex segment
            hex_bytes = part.strip().split()
            binary_segment = b""
            for hex_byte in hex_bytes:
                binary_segment += binascii.unhexlify(hex_byte)
            segments.append(binary_segment)
        elif part:
            # Handle text segment
            segments.append(part.encode())

    return segments

def create_payload(segments):
    payload = b""
    for segment in segments:
        payload += segment + b""
    return payload

def send_content(Protocol, src_ip, src_port, dst_ip, dst_port, content, flow):
    global icmp_index
    global tcp_index
    global udp_index
    ip_layer = IP(src=str(src_ip), dst=str(dst_ip))
    if content:
        content_convert = split_and_convert(content)
        print(f"content_convert: {content_convert}")
        payload = create_payload(content_convert)
        print(f"payload: {payload}")
    else:
        print("payload is empty")
        payload = ""
    if Protocol == "icmp":
        packet = ip_layer / ICMP()
        if icmp_index == 0 or tcp_index == 0 or udp_index == 0:
            folders()
        wrpcap(f"pcaps/icmp/{str(icmp_index)}.pcap", packet)
        icmp_index += 1
    elif Protocol == "tcp":
        tcp_layer = TCP(sport=int(src_port), dport=int(dst_port), flags='PA')
        packet = ip_layer / tcp_layer / Raw(load=payload)
        if tcp_index == 0 or tcp_index == 0 or udp_index == 0:
            folders(flow)
        if flow is not None:
            wrpcap(f"pcaps/tcp/{str(flow)}/{str(tcp_index)}.pcap", packet)
        else:
            wrpcap(f"pcaps/tcp/undefined_flow/{str(tcp_index)}.pcap", packet)
        tcp_index += 1
    elif Protocol == "udp":
        udp_layer = UDP(sport=int(src_port), dport=int(dst_port)) / Raw(load=payload)
        packet = ip_layer / udp_layer / Raw(load=payload)
        if udp_index == 0 or tcp_index == 0 or udp_index == 0:
            folders()
        wrpcap(f"pcaps/udp/{str(udp_index)}.pcap", packet)
        
        
def main():
    while True:
        wordlist = sys.stdin.readline()
        wordlist = str(wordlist)
        pattern_flow = r'flow:(.*?);'
        pattern_content = r'content:"(.*?)";\s*(?:distance:(\d+);)?\s*(?:within:(\d+);)?'
        pattern_reference = r'reference:(.*?);'
        pattern_classtype = r'classtype:(.*?);'
        pattern_sid = r'sid:(\d+);'
        pattern_rev = r'rev:(\d+);'
        pattern_metadata = r'metadata:(.*?);'

        Rule_header = re.split(r'\(.*\)', wordlist)
        Rule_header = Rule_header[0].strip()
        Rule_header = [part.strip() for part in Rule_header.split(' ') if part != '->']
        Action = str(Rule_header[0])
        Protocol = str(Rule_header[1])
        Source_address = str(Rule_header[2])
        Source_port = str(Rule_header[3])
        Destination_address = str(Rule_header[4])
        Destination_port = str(Rule_header[5])

        flow_match = re.search(pattern_flow, wordlist)
        flow = flow_match.group(1) if flow_match else None
        if flow:
            flow = flow.replace("(", "").replace(")", "")
        Content = []
        Distance = []
        Within = []
        content_matches = re.findall(pattern_content, wordlist)
        for match in content_matches:
            Content.append(f"{match[0]}")
            Distance.append(match[1] if match[1] else "#")
            Within.append(match[2] if match[2] else "#")

        reference_match = re.search(pattern_reference, wordlist)
        reference = reference_match.group(1) if reference_match else None

        classtype_match = re.search(pattern_classtype, wordlist)
        classtype = classtype_match.group(1) if classtype_match else None

        sid_match = re.search(pattern_sid, wordlist)
        sid = sid_match.group(1) if sid_match else None

        rev_match = re.search(pattern_rev, wordlist)
        rev = rev_match.group(1) if rev_match else None

        metadata_match = re.search(pattern_metadata, wordlist)
        metadata = metadata_match.group(1) if metadata_match else None

        print(f"Action: {Action}")
        print(f"Protocol: {Protocol}")
        print(f"Source_address: {Source_address}")
        print(f"Source_port: {Source_port}")
        print(f"Destination_address: {Destination_address}")
        print(f"Destination_port: {Destination_port}")
        print(f"Flow: {flow}")
        print(f"Content: {Content}")
        print(f"Distance: {Distance}")
        print(f"Within: {Within}")
        print(f"Reference: {reference}")
        print(f"Classtype: {classtype}")
        print(f"SID: {sid}")
        print(f"Rev: {rev}")
        print(f"Metadata: {metadata}")
        
        if Source_address == Destination_address:
            print("wrong addressation !!!!!!!!!!!!!!!!!!")
            continue
        
        # Content parsing
        content_end = ""
        character_flag = False # if "|" exists
        for word in Content:
            if word.startswith('|') and word.endswith('|'):
                if Content.index(word) == 0:
                    content_end += word[:-1]
                elif character_flag == True:
                    character_flag = False
                    if Distance[Content.index(word)].isdigit() == True and int(Distance[Content.index(word)]) >= 1:
                        content_end += " aa" * int(Distance[Content.index(word)])
                    content_end += word[:-1]
                else:
                    if Distance[Content.index(word)].isdigit() == True and int(Distance[Content.index(word)]) >= 1:
                        content_end += " aa" * int(Distance[Content.index(word)])
                    content_end += " " + word[1:-1]
            else:
                if Content.index(word) == 0:
                    if word[-1] == "|":
                        content_end += word[:-1]
                    else:
                        content_end += word
                        character_flag = True
                else:
                    if Distance[Content.index(word)].isdigit() == True and int(Distance[Content.index(word)]) >= 1:
                        content_end += " aa" * int(Distance[Content.index(word)])
                    if word[0] != "|" and word[-1] != "|":
                        content_end += " " + word
                        character_flag == True
                    elif word[0] != "|" and word[-1] == "|":
                        content_end += " " + word[:-1]
                    else:
                        content_end += " " + word[1:]
                    character_flag = True
            if Content.index(word) == len(Content) - 1 and word[-1] == "|":
                content_end += "|"
                
        # test purpose
        print(f"contend_end: {content_end}")

            
        send_content(Protocol, Source_address, Source_port, Destination_address, Destination_port, content_end, flow)



main()