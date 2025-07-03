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

DEFAULT_N_THREADS = 50
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

def scan_thread(host):
    global q
    while True:
        # get port num from queue
        worker = q.get()
        # scan the port number we just got from the queue
        port_scan(host, worker)
        # tells queue the current port scan is done
        q.task_done()

def main(host, ports, n_threads):
    global q
    for t in range(n_threads):
        t = Thread(target=scan_thread, args=(host,))
        # when daemon set to true, current thread ends when main thread ends
        t.daemon = True
        # start deamon thread
        t.start()
    for worker in ports:
        # for each port put that port into the queue to start scanning
        q.put(worker)
    # wait for threads to finish
    q.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple port scanner")
    parser.add_argument("host", help="Required argument, this is the host to scan.")
    parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="Port range to scan, default is 1-65535 (all ports)")
    parser.add_argument("--threads", "-n", "-t", dest="n_threads", default=50, help="Number of threads, default is 50")
    args = parser.parse_args()
    host, port_range, n_threads = args.host, args.port_range, args.n_threads

    start_port, end_port = port_range.split("-")
    start_port, end_port = int(start_port), int(end_port)

    ports = [ p for p in range(start_port, end_port)]

    n_threads = int(n_threads)

    main(host, ports, n_threads)