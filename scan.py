import socket

target = input("Enter target (e.g. scanme.nmap.org): ")
ports = [22, 80, 443, 21, 25]

print(f"Scanning {target}...")
for port in ports:
    s = socket.socket()
    s.settimeout(1)
    result = s.connect_ex((target, port))
    if result == 0:
        print(f"[+] Port {port} is OPEN")
    else:
        print(f"[-] Port {port} is closed")
    s.close()
print("Scan done!")
