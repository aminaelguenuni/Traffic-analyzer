# Network Traffic Analyzer — Wireshark + Python
 
A small command-line tool that reads a captured network traffic file (`.pcap`/`.pcapng`) and flags suspicious patterns automatically, so you're not stuck scrolling through thousands of packets in Wireshark trying to spot something manually.
 
It works by:
- Capturing traffic with Wireshark (the GUI does the actual capturing)
- Reading that capture into Python with `pyshark`
- Running a couple of detection rules on the TCP and ARP traffic as it streams by
The goal is simple: **out of everything that crossed this network, what actually looks suspicious?**
 
Tested against a self-captured `.pcapng` file of normal browsing traffic (~38,600 packets).
 
## Features
 
**Reads a capture file**
Loads a `.pcap`/`.pcapng` file (captured separately in Wireshark's GUI) and streams through every packet in a single pass.
 
**Counts packets**
Reports the total number of packets read, just so you have a sense of how much traffic you're looking at.
 
**Port scan detection**
Watches for TCP SYN packets sent without a matching ACK, per source IP. If one IP sends a lot of these (default: more than 15) without ever completing a real connection, that's the classic signature of someone scanning ports, and it gets flagged.
 
**ARP spoofing detection**
Keeps track of which MAC address(es) have claimed each IP seen in ARP traffic. Normally, one IP is always claimed by the same MAC. If two different MACs both claim the same IP, that's a red flag — usually a sign of a man-in-the-middle setup on the local network.
 
## Example Output
 
```
Opening sample.pcapng ...
Total packets read: 38614
 
No suspicious patterns detected.
```
 
Or, if something's actually flagged:
 
```
Suspicious patterns found:
[PORT SCAN?] 192.168.1.23 sent 47 SYN packets with no completed handshake
[ARP SPOOF?] 192.168.1.1 claimed by multiple MACs: {'aa:bb:cc:dd:ee:ff', '11:22:33:44:55:66'}
```
 
## Project Structure
 
| File | Description |
|---|---|
| `analyzer.py` | The whole thing — loads the capture, runs the checks, prints what it finds |
| `sample.pcapng` | Example capture used for testing |
 
## Usage
 
Capture some traffic first using Wireshark's GUI, and save it into the project folder (e.g. as `sample.pcapng`).
 
Then run:
 
```
python analyzer.py sample.pcapng
```
 
It'll print the total packet count, then any suspicious patterns it found — or let you know if it didn't find anything.
 
## Requirements
 
- [Wireshark](https://www.wireshark.org/) installed (this gives you `tshark`, which `pyshark` uses under the hood)
- `pip install pyshark`
## What's not built yet
 
A couple of things from the original plan aren't in here yet:
- Catching plaintext credentials in HTTP/FTP/Telnet traffic
- Flagging unusually high DNS query volume (possible tunneling)
- Live capture mode, instead of only working on saved files
Might add these later — for now the focus was getting port scan and ARP spoof detection working properly.
 
## Author
 
Created by Amina El Guenuni.
 
