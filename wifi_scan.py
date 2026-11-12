import socket
import threading
import subprocess
from queue import Queue

print("Getting your WiFi network...")

# Get your own IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()
except:
    my_ip = "192.168.1.100"

print(f"Your IP: {my_ip}")
# Get network base, e.g. 192.168.1.
base = ".".join(my_ip.split(".")[:3]) + "."
print(f"Scanning {base}1 to {base}254...\n")

q = Queue()
found = []

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown"

def ping(ip):
    # Use ping, 1 packet, 1 sec timeout
    result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        hostname = get_hostname(ip)
        print(f"[+] {ip} ONLINE - {hostname}")
        found.append(ip)

def worker():
    while not q.empty():
        ip = q.get()
        ping(ip)
        q.task_done()

for i in range(1, 255):
    q.put(base + str(i))

threads = []
for _ in range(30):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

q.join()
print(f"\nDone! Found {len(found)} devices on your WiFi.")
try:
    import os
    os.system(f'termux-tts-speak "wifi scan complete, found {len(found)} devices"')
    os.system('termux-vibrate -d 500')
    os.system(f'termux-notification --title "WiFi Scan Done" --content "Found {len(found)} devices"')
except:
    pass
