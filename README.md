# Network Traffic Analyzer: Wireshark + Python
 
A command-line tool that reads a captured network traffic file (`.pcap`/`.pcapng`) and flags suspicious patterns automatically, so you're not stuck scrolling through thousands of packets in Wireshark trying to spot something manually.
 
It works by:
- Capturing traffic with Wireshark (the GUI does the actual capturing)
- Reading that capture into Python with `pyshark`
- Running a couple of detection rules on the TCP and ARP traffic as it streams by
 
Tested against a self-captured `.pcapng` file of normal browsing traffic (~38,600 packets).
 
## Features
 
**Reads a capture file**
Loads a `.pcap`/`.pcapng` file (captured separately in Wireshark's GUI) and streams through every packet in a single pass.
 
**Counts packets**
Reports the total number of packets read, just so you have a sense of how much traffic you're looking at.
 
**Port scan detection**
Watches for TCP SYN packets sent without a matching ACK, per source IP. If one IP sends a lot of these (default: more than 15) without ever completing a real connection, that's the classic signature of someone scanning ports, and it gets flagged.
 
**ARP spoofing detection**
Keeps track of which MAC address(es) have claimed each IP seen in ARP traffic. Normally, one IP is always claimed by the same MAC. If two different MACs both claim the same IP, that's a red flag.
 
## Example Output
 
```
Opening sample.pcapng ...
Total packets read: 38614
 
No suspicious patterns detected.
```

## Usage
 
Capture some traffic first using Wireshark's GUI, and save it into the project folder (e.g. as `sample.pcapng`).
 
Then run:
 
```
python analyzer.py sample.pcapng
```
 
It'll print the total packet count, then any suspicious patterns it found, or let you know if it didn't find anything.
 
## Requirements
 
- [Wireshark](https://www.wireshark.org/) installed (this gives you `tshark`, which `pyshark` uses under the hood)
- `pip install pyshark`

## Author
 
Created by Amina El Guenuni.
 
