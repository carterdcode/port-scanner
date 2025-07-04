# A python port scanning program, built upon from https://thepythoncode.com/article/make-port-scanner-python
import argparse
import socket
import sys
from colorama import init, Fore
from threading import Thread, Lock
from queue import Queue

init()
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

DEFAULT_N_THREADS = 50
# thread queue
q = Queue()
print_lock = Lock()

# Display options (will be set from command line)
show_closed = None
show_filtered = None

# Track filtered ports for retry option
filtered_ports = []
filtered_lock = Lock()

def port_scan(host, port, timeout=3):
    global show_closed, show_filtered, filtered_ports, filtered_lock
    try:
        s = socket.socket()
        s.settimeout(timeout)  # Configurable timeout
        s.connect((host, port))
    except socket.timeout:
        # Timeout usually indicates filtered port (firewall dropping packets)
        with filtered_lock:
            filtered_ports.append(port)
        if show_filtered:
            with print_lock:
                print(f"{YELLOW}{host:15}:{port:5} may be filtered (timeout) {RESET}")
    except socket.error as e:
        # Connection refused = closed port
        if e.errno in [10061, 111]:  # Connection refused (Windows/Linux)
            if show_closed:
                with print_lock:
                    print(f"{GRAY}{host:15}:{port:5} is closed  {RESET}")
        else:
            # Other socket errors might indicate filtering
            with filtered_lock:
                filtered_ports.append(port)
            if show_filtered:
                with print_lock:
                    print(f"{YELLOW}{host:15}:{port:5} may be filtered ({e}) {RESET}")
    except Exception as e:
        # Unexpected errors
        with print_lock:
            print(f"{RED}{host:15}:{port:5} error: {e} {RESET}")
    else:
        # Connection successful = open port
        with print_lock:
            print(f"{GREEN}{host:15}:{port:5} is open    {RESET}")
    finally:
        s.close()

def scan_thread(host, timeout=3):
    global q
    while True:
        # get port num from queue
        worker = q.get()
        # scan the port number we just got from the queue
        port_scan(host, worker, timeout)
        # tells queue the current port scan is done
        q.task_done()

def main(host, ports, n_threads):
    global q
    print(f"Starting scan...")
    
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
    
    print(f"\nScan completed! Scanned {len(ports)} ports on {host}")

if __name__ == "__main__":   
    parser = argparse.ArgumentParser(description="Simple port scanner")
    parser.add_argument("host", help="Required argument, this is the host to scan.")
    parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="Port range to scan, default is 1-65535 (all ports)")
    parser.add_argument("--threads", "-n", "-t", dest="n_threads", default=50, help="Number of threads, default is 50")
    parser.add_argument("--show-closed", "-c", action="store_true", help="Show closed ports (creates lots of output)")
    parser.add_argument("--show-filtered", "-f", action="store_true", default=True, help="Show filtered ports (default: True)")
    args = parser.parse_args()
    host, port_range, n_threads = args.host, args.port_range, args.n_threads
    
    show_closed = args.show_closed
    show_filtered = args.show_filtered

    start_port, end_port = port_range.split("-")
    start_port, end_port = int(start_port), int(end_port)

    ports = [p for p in range(start_port, end_port + 1)]  # Include end port

    n_threads = int(n_threads)
    
    print(f"Scanning {host} ports {start_port}-{end_port} with {n_threads} threads...")
    display_info = []
    if show_closed: display_info.append("closed")
    if show_filtered: display_info.append("filtered") 
    display_info.append("open")
    print(f"Displaying: {', '.join(display_info)} ports\n")

    main(host, ports, n_threads)