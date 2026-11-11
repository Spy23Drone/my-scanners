import socket

target = input("Enter target: ")
start = int(input("Start port: "))
end = int(input("End port: "))

print(f"Scanning {target} from {start} to {end}...")
for port in range(start, end+1):
    s = socket.socket()
    s.settimeout(0.5)
    result = s.connect_ex((target, port))
    if result == 0:
        print(f"[+] Port {port} is OPEN")
    s.close()
print("Scan done!")
