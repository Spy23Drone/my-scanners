import socket
import threading
from queue import Queue

target = input("Target IP or domain: ")
try:
    ip = socket.gethostbyname(target)
    print(f"Scanning {target} ({ip})...")
except:
    print("Could not resolve target")
    exit()

q = Queue()
open_ports = []

def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        result = s.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            print(f"[+] Port {port} OPEN - {service}")
            open_ports.append(port)
        s.close()
    except:
        pass

def worker():
    while not q.empty():
        port = q.get()
        scan(port)
        q.task_done()

# Put ports 1-1024 in queue
for p in range(1, 1025):
    q.put(p)

# 50 threads = fast
threads = []
for _ in range(50):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

q.join()
print(f"\nDone! Found {len(open_ports)} open ports: {open_ports}")
