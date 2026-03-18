######################################################################################################
# Port Scanner by Spencer Rich
# This is a basic TCP port scanner I built with help from an online article. The purpose
# of this project was primarily to familiarize myself with network scanning and refresh
# my python knowledge. Note that this software uses threading to increase performance - modify
# max_workers to increase or decrease the upper bound of the concurrent threads. Additionally, 
# TIMEOUT can be changed to determine how long the program waits before moving on to the next port.
# For simplicity and speed, only open ports are printed to output.
#
# Should you choose to use this scanner, be sure to follow your network's acceptable use policies
# and legal guidelines.
######################################################################################################

# Import Python modules
import sys
import socket
import time
import errno
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

TIMEOUT = 0.5

# Define a target
if len(sys.argv) == 2:
    # Translate hostname to IPv4
    try:
        target = socket.gethostbyname(sys.argv[1])
    except socket.gaierror:
        print("Hostname could not be resolved")
        sys.exit()

else:
    print("Please add a target hostname or IP address")
    sys.exit()

# Show scan info
print("=" * 49)
print("||Scan Target: " + target + "                   ||")
print("||Scanning started: " + str(datetime.now()) + " ||")
print("=" * 49)

# Scan function
def scan_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(TIMEOUT)

        start = time.time()
        result = s.connect_ex((target, port))
        duration = time.time() - start

        if result == 0:
            print(f"Port {port} is open")
        
        elif result == errno.ECONNREFUSED:
            print(f"Port {port} is closed")
        
        elif duration >= TIMEOUT:
            print(f"Port {port} is filtered (timeout)")
        
        else:
            print(f"Port {port} is filtered/unknown")

# Run the scan
try:
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(scan_port, range(1, 1000))

# Exception handling for scan inturrupt
except KeyboardInterrupt:
    print("\n Scan halted by user")
    sys.exit()

# General exception handling
except Exception as e:
    print("Error: ", e)

# Debug
print("Program has ended")
