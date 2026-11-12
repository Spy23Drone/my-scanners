import glob
code = '''
try:
    import os
    os.system('termux-tts-speak "scan complete"')
    os.system('termux-vibrate -d 500')
except:
    pass
'''
for f in glob.glob("*.py"):
    if f in ["add_api.py", "wifi_scan.py", "subdomain_scan.py"]:
        continue
    data = open(f).read()
    if "termux-tts-speak" not in data:
        open(f, "a").write(code)
        print(f"Patched {f}")
print("Done!")
