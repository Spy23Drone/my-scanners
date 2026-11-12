import socket
from concurrent.futures import ThreadPoolExecutor

target = input("Enter target: ")

def check(port):
    s = socket.socket()
    s.settimeout(1)
    if s.connect_ex((target, port)) == 0:
        print(f"[+] Port {port} is OPEN")
    s.close()

print(f"Scanning {target} fast...")
with ThreadPoolExecutor(max_workers=50) as ex:
    ex.map(check, range(1, 101))
print("Scan done!")

try:
    import os
    os.system('termux-tts-speak "scan complete"')
    os.system('termux-vibrate -d 500')
except:
    pass
