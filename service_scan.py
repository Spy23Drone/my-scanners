import socket
import threading
from queue import Queue

target = input("Target: ")
try:
    ip = socket.gethostbyname(target)
    print(f"Scanning {target} ({ip})...")
except:
    print("Could not resolve target")
    exit()

q = Queue()

def get_banner(s, port):
    try:
        s.settimeout(1.0)
        # Try to grab banner
        banner = s.recv(1024).decode(errors="ignore").strip()
        if banner:
            return banner.splitlines()[0][:80]
    except:
        pass
    # If no banner, try sending HTTP probe for web ports
    if port in [80, 8080, 8000, 8888]:
        try:
            s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode(errors="ignore").strip()
            if banner:
                return banner.splitlines()[0][:80]
        except:
            pass
    return "No banner"

def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        if s.connect_ex((ip, port)) == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            banner = get_banner(s, port)
            print(f"[+] {port} OPEN - {service} | {banner}")
        s.close()
    except:
        pass

def worker():
    while not q.empty():
        port = q.get()
        scan(port)
        q.task_done()

# Common ports - faster than 1-1024 and more useful
ports = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5432,5900,8000,8080,8443,8888]
for p in ports:
    q.put(p)

threads = []
for _ in range(20):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

q.join()
print("\nDone! Service scan complete.")
try:
    import os
    os.system('termux-tts-speak "service scan complete"')
    os.system('termux-vibrate -d 500')
    os.system('termux-notification --title "Scan Done" --content "Service scan finished"')
except:
    pass
