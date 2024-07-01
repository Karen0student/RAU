import re
from scapy.all import IP, TCP, ICMP, UDP, wrpcap, sendp, rdpcap, send, Raw, sr1, sniff, sr
import binascii
import sys
import os
import random

icmp_index = 0
tcp_index = 0
udp_index = 0

def parse_ipvars_portvars(conf_text): # parse from snort.conf
    vars = {}
    lines = conf_text.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('ipvar') and '#' not in line:
            parts = line.split()
            if len(parts) >= 3:
                var_name = parts[1]
                var_value = parts[2]
                vars[var_name] = var_value
            else:
                print("!!!WRONG CONFIGS!!!")
        elif line.startswith('portvar') and '#' not in line:
            parts = line.split() 
            if len(parts) >= 3:
                var_name = parts[1]
                var_value = parts[2]
                vars[var_name] = var_value
            else:
                print("!!!WRONG CONFIGS!!!")
    

    for key, value in vars.items(): # reads as str, so we changing to list
        if value.startswith('['):
            vars[key] = vars[key].split(',')
            vars[key][0] = vars[key][0].replace('[', '')
            vars[key][-1] = vars[key][-1].replace(']', '')

    resolved_ipvars = {}
    for key, value in vars.items():
        if isinstance(value, list): # if we have list of values from $variables
            value_list = []
            for element in value:
                if element.startswith('$'):
                    ref_var_key = element[1:]
                    ref_value = vars.get(ref_var_key, element)
                    value_list.append(ref_value)
                else:
                    value_list.append(element)
            merge_list = []
            for item in value_list: # merging lists in list
                # If the item is a list, extend the merge_list with its elements
                if isinstance(item, list):
                    merge_list.extend(item)
                else:
                    # Otherwise, append the item itself to the merge_list
                    merge_list.append(item)
            resolved_ipvars[key] = merge_list
        elif value.startswith('$'):
            ref_var_key = value[1:]
            ref_value = vars.get(ref_var_key, value)
            resolved_ipvars[key] = ref_value
        else:
            resolved_ipvars[key] = value
    return resolved_ipvars


def extract_content(string):
    content_flag = False
    distance_flag = False
    within_flag = False
    everything = []
    flow = ""
    content = []
    distance = []
    within = []
    sid = ""
    rev = ""
    parts = string.split('(')
    for part in parts:
            attributes = part.split(';')
            for attribute in attributes:
                if 'sid:' in attribute:
                    sid += attribute.split(':')[1].strip('"')
                    continue
                if 'rev:' in attribute:
                    rev += attribute.split(':')[1].strip('"')
                    continue
                if 'flow:' in attribute:
                    flow += attribute.split(':')[1].strip('"')
                    continue
                
                if content_flag is True:
                    if 'distance:' in attribute:
                        distance.append(attribute.split(':')[1].strip('"'))
                        distance_flag = True
                        continue
                    elif 'within:' in attribute:
                        within.append(attribute.split(':')[1].strip('"'))
                        within_flag = True
                        continue
                    elif 'nocase' in attribute:
                        continue
                    else:
                        content_flag = False
                        if distance_flag is True:
                            distance_flag = False
                        else:
                            distance.append("#")
                        if within_flag is True:
                            within_flag = False
                        else:
                            within.append("#")
                if 'content:' in attribute:
                    content.append(attribute.split(':')[1].strip('"'))
                    content_flag = True
                    continue
    distance.append('#') # additional
    within.append('#') # additional
    if flow == "":
        flow = None
    if sid == "":
        sid = None
    if rev == "":
        rev = None
    everything.append(flow)
    everything.append(content)
    everything.append(distance)
    everything.append(within)
    everything.append(sid)
    everything.append(rev)
    return everything



def folders(flow=""): # creating folders for sorting packets
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
    parts = text.strip().split("|")
    for part in parts:
        if all(c in '0123456789abcdefABCDEF ' for c in part) and len(part.strip()) != 1:
            # Handle hex segment
            hex_bytes = part.strip().split()
            binary_segment = b""
            for hex_byte in hex_bytes:
                if len(hex_byte) > 2: # if there is string in lowercase and not hex type 
                    segments.append(part.encode())
                    continue
                try:
                    binary_segment += binascii.unhexlify(hex_byte)
                except binascii.Error as e:
                    print("!!!!!HEX TEXT ENCODING ERROR, SKIPPING!!!!!")
                    return None
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
    if src_ip == "any":
        src_ip = "192.168.0." + str(random.randint(1, 254))
    if dst_ip == "any":
        dst_ip = "192.168.0." + str(random.randint(1, 254))
    if src_port == "any":
        src_port = int(random.randint(1, 65535))
    if dst_port == "any":
        dst_port = int(random.randint(1, 65535))
        
    ip_layer = IP(src=str(src_ip), dst=str(dst_ip))
    if content:
        content_convert = split_and_convert(content)
        if content_convert is None:
            return
        print(f"content_convert: {content_convert}")
        payload = create_payload(content_convert)
        print(f"payload: {payload}")
    else:
        print("payload is empty")
        payload = ""
    
    if Protocol == "icmp":
        packet = ip_layer / ICMP()
        folders()
        wrpcap(f"pcaps/icmp/{str(icmp_index)}.pcap", packet)
        icmp_index += 1
    
    elif Protocol == "tcp":
        tcp_layer = TCP(sport=int(src_port), dport=int(dst_port), flags='PA')
        packet = ip_layer / tcp_layer / Raw(load=payload)
        folders(flow)
        if flow is not None:
            wrpcap(f"pcaps/tcp/{str(flow)}/{str(tcp_index)}.pcap", packet)
        else:
            wrpcap(f"pcaps/tcp/undefined_flow/{str(tcp_index)}.pcap", packet)
        tcp_index += 1
    
    elif Protocol == "udp":
        udp_layer = UDP(sport=int(src_port), dport=int(dst_port)) / Raw(load=payload)
        packet = ip_layer / udp_layer / Raw(load=payload)
        folders()
        wrpcap(f"pcaps/udp/{str(udp_index)}.pcap", packet)
        udp_index += 1
        
        
def main():
    with open("/etc/snort/snort.conf") as file:
        vars = parse_ipvars_portvars(file.read())
        print(vars)

    while True:
        wordlist = sys.stdin.readline()
        if wordlist == "":
            print("Done")
            break
        wordlist = str(wordlist)
        extracted_content = extract_content(wordlist)
        Rule_header = re.split(r'\(.*\)', wordlist)
        Rule_header = Rule_header[0].strip()
        Rule_header = [part.strip() for part in Rule_header.split(' ') if part != '->' and part != '<>']
        Action = str(Rule_header[0])
        Protocol = str(Rule_header[1])
        Source_address = str(Rule_header[2])
        Source_port = str(Rule_header[3])
        Destination_address = str(Rule_header[4])
        Destination_port = str(Rule_header[5])
        flow = extracted_content[0]
        Content = extracted_content[1]
        Distance = extracted_content[2]
        Within = extracted_content[3]
        sid = extracted_content[4]
        rev = extracted_content[5]
        
        Content = [item for item in Content if item != '']
        print("------------------------------------------------")
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
        print(f"SID: {sid}")
        print(f"Rev: {rev}")
        # resolve Source_address, Source_port, Destination_address, Destination_port values
        if Source_address.startswith('!') or Destination_address.startswith('!') or \
        Source_port.startswith('!') or Destination_port.startswith('!'):
            print("CAN'T HANDLE '!' OPTION, SKIPPING !!!")
            continue
        
        if Source_address.startswith('['):
            Source_address = Source_address.strip('[]').split(',')[0]
        if Source_address.startswith('$'):
            Source_address = vars[Source_address[1:]]
        Source_address = Source_address.lower()
        print(f"SOURCE_ADDRESS: {Source_address}")
        if Destination_address.startswith('['):
            Destination_address = Destination_address.strip('[]').split(',')[0]
        if Destination_address.startswith('$'):
            Destination_address = vars[Destination_address[1:]]
        Destination_address = Destination_address.lower()
        print(f"DESTINATION_ADDRESS: {Destination_address}")
        # if Source_address == Destination_address:
        #     print("wrong addressation!")
        #     continue
        if Source_port.startswith('['):
            Source_port = Source_port.strip('[]').split(',')[0]
        if Source_port.startswith('$'):
            Source_port = vars[Source_port[1:]]
            if isinstance(Source_port, list):
                Source_port = Source_port[0]
        if ':' in Source_port:
            Source_port = Source_port.split(':')[0]
        ## if , or : in ports, skip
        if ',' in Source_port or ':' in Source_port:
            print("!!!!!WRONG SOURCE_PORT SYNTAX, SKIPPING!!!!!")
            continue
        Source_port = Source_port.lower()
        print(f"SOURCE_PORT: {Source_port}")
        
        if Destination_port.startswith('['):
            Destination_port = Destination_port.strip('[]').split(',')[0]
        if Destination_port.startswith('$'):
            Destination_port = vars[Destination_port[1:]]
            if isinstance(Destination_port, list):
                Destination_port = Destination_port[0]
        if ':' in Destination_port:
            Destination_port = Destination_port.split(':')[0]
        if ',' in Destination_port or ':' in Destination_port:
            print("!!!!!WRONG DESTINATION_PORT SYNTAX, SKIPPING!!!!!")
            continue
        Destination_port = Destination_port.lower()
        print(f"DESTINATION_PORT: {Destination_port}")
        
        if not Source_port.isdigit() and len(Source_port) == 1: # if junk
            print("!!!!!WRONG PORT INPUT!!!!!")
            continue
        if not Destination_port.isdigit() and len(Destination_port) == 1: # if junk
            print("!!!!!WRONG PORT INPUT!!!!!")
            continue
        
        # Content parsing
        content_end = ""
        if Content:
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
