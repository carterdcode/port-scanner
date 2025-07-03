import socket
import sys
from colorama import init, Fore

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

def is_port_open(host, port):
    s = socket.socket()
    try:
        s.connect((host,port))
    except:
        # cannot connect/port is closed
        return False
    else:
        # connection established/port is open
        return True

if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    host = input("Enter Host IP")

for port in range(1, 1025):
    if is_port_open(host, port):
        print(f"{GREEN}[+] {host}:{port} is open      {RESET}")
    else:
        print(f"{GRAY}[!] {host}:{port} is closed    {RESET}", end="\r")