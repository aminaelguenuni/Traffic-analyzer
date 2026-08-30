import sys
import pyshark
import asyncio
from collections import defaultdict

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
# open the capture and count packets
def load_capture(path): #load the capture file using pyshark
    return pyshark.FileCapture(path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <capture_file>")
        sys.exit(1)

    file_path = sys.argv[1] #making sure the user has provided a file path 
    print(f"Opening {file_path} ...")

    capture = load_capture(file_path)#open file 

    total_count = 0
    syn_counts = defaultdict(int)# a dict where each IP starts at 0
    ip_to_macs = defaultdict(set)# a dict where each IP maps to a set of MACs
    SYN_THRESHOLD = 15 #cutoff 

    for packet in capture:
        total_count += 1

        # port scan check
        try:
            if hasattr(packet, 'tcp'):
                if packet.tcp.flags_syn == '1' and packet.tcp.flags_ack == '0':
                    syn_counts[packet.ip.src] += 1
        except AttributeError:
            pass

        # ARP spoofing check
        if hasattr(packet, 'arp'):
            ip_to_macs[packet.arp.src_proto_ipv4].add(packet.arp.src_hw_mac)

    print(f"Total packets read: {total_count}")

    findings = []

    for ip, count in syn_counts.items(): #checks every IP count against threshold
        if count > SYN_THRESHOLD:
            findings.append(f"[PORT SCAN?] {ip} sent {count} SYN packets with no completed handshake")

    for ip, macs in ip_to_macs.items():#check every IP set of MACs
        if len(macs) > 1:#more than one MAC claimed that IP: red flag 
            findings.append(f"[ARP SPOOF?] {ip} claimed by multiple MACs: {macs}")

    if findings:#printing results 
        print("\nSuspicious patterns found:")
        for f in findings:
            print(f)
    else:
        print("\nNo suspicious patterns detected.")

   