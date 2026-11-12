import socket
import threading
from queue import Queue
domain = input("Domain: ").strip()
print(f"Scanning {domain}...")
words = ["www","mail","ftp","admin","api","blog","dev","test","shop","app","portal","login","secure","vpn","webmail","cdn","support","help","staging","beta"]
q = Queue()
for w in words:
    q.put(w)
def worker():
    while not q.empty():
        sub = q.get()
        full = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(full)
            print(f"[+] {full} -> {ip}")
        except:
            pass
        q.task_done()
threads = []
for _ in range(15):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)
q.join()
print("Done!")
