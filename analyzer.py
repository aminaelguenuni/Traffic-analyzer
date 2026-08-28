import sys
import pyshark
import asyncio
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

    capture = load_capture(file_path)

    count = 0 #counting the packets in the capture file 
    for packet in capture:
        count += 1

    print(f"Total packets read: {count}")