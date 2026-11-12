import socket

target = input("Enter target: ")
port = int(input("Enter port: "))

s = socket.socket()
s.settimeout(2)
s.connect((target, port))
s.send(b"Hello\r\n")
banner = s.recv(1024)
print(f"Banner on port {port}: {banner.decode(errors='ignore')}")
s.close()

try:
    import os
    os.system('termux-tts-speak "scan complete"')
    os.system('termux-vibrate -d 500')
except:
    pass
