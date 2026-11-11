import socket
from concurrent.futures import ThreadPoolExecutor

target = input("Enter target: ")

def check(port):
    s = socket.socket()
    s.settimeout(1)
    try:
        s.connect((target, port))
        s.send(b"Hello\r\n")
        banner = s.recv(1024).decode(errors='ignore').strip()
        print(f"[+] Port {port} OPEN - {banner}")
    except:
        pass
    s.close()

print(f"Scanning {target}...")
with ThreadPoolExecutor(max_workers=50) as ex:
    ex.map(check, range(1, 101))
print("Scan done!")
