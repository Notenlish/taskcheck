import psutil
import time
import winreg
import subprocess
import os

app_path = os.path.abspath(__file__)

key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
winreg.SetValueEx(key, 'AppDefender', 0, winreg.REG_SZ, app_path)
key.Close()

try:
    with open("banned_files", "r") as f:
        banned = f.readlines()
    for i, b in enumerate(banned):
        banned[i] = b.strip()
except:
    banned = []
    with open("banned_files", "w") as f:
        data = ""
        for d in banned:
            data += "\n" + str(d)
        f.write(data)

def run():
    while True:
        for proc in psutil.process_iter():
            name = proc.name().strip()
            if name == "javaw.exe":
                print(dir(proc))
                childrens = proc.children(recursive=True)
                parents = proc.parents()
                print(childrens, parents, sep="\n\n")
            for bannedproc in banned:
                if name in bannedproc:
                    print(f"killed {name}")
                    try:
                        proc.kill()
                    except psutil.NoSuchProcess:
                        pass
        time.sleep(5)

def run2():
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description,Id,Path'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if not line.decode()[0].isspace():
            print(line.decode().rstrip())

# https://stackoverflow.com/questions/54827918/get-list-of-running-windows-applications-using-python
# https://www.geeksforgeeks.org/python-get-list-of-running-processes/

if __name__ == '__main__':
    run2()