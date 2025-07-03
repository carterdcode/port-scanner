import argparse
import socket
import sys
from colorama import init, Fore
from threading import Thread, Lock
from queue import Queue

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

N_THREADS = 200
# thread queue
q = Queue()
print_lock = Lock()

def port_scan(host, port):
    try:
        s = socket.socket()
        s.connect((host,port))
    except: 
        with print_lock:
            print(f"{GRAY}{host:15}:{port:5} is closed  {RESET}", end='\r')
    else:
        with print_lock:
            print(f"{GREEN}{host:15}:{port:5} is open    {RESET}")
    finally:
        s.close()

def scan_thread():
    global q
    while True:
        # get port num from queue
        worker = q.get()
        # scan the port number we just got from the queue
        port_scan(host, worker)
        # tells queue the current port scan is done
        q.task_done()

def main(host, ports):
    global q
    for t in range(N_THREADS):
        t = Thread(target=scan_thread)
        # when daemon set to true, current thread ends when main thread ends
        t.daemon = True
        # start deamon thread
        t.start()
    for worker in ports:
        # for each port put that port into the queue to start scanning
        q.put(worker)
    # wait for threads to finish
    q.join()

if (len(sys.argv) >1 ):
    host, ports = sys.argv[1], sys.argv[2]
    start_port, end_port = ports.split("-")
    start_port, end_port = int(start_port), int(end_port)
else:
    print(sys.argv)
    host, ports = input("Enter args in format HostIP StartPort-EndPort").split(" ")
    #get the start and end ports
    start_port,end_port = ports.split("-")
    start_port, end_port = int(start_port), int(end_port)

ports = [ p for p in range(start_port, end_port)]

main(host, ports)