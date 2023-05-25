import psutil
import time
import winreg
import subprocess
import os
import sys

def add_to_startup():
    path = os.path.abspath(sys.argv[0])     
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, 'AppDefender', 0, winreg.REG_SZ, path)
    winreg.CloseKey(key)

add_to_startup()

BASE_BANNED_APPS = """RiotClientUx.exe
RiotClient.exe
RiotClientUxRender.exe
RiotClientCrashHandler.exe
BlueStacks X.exe
BlueStacksWeb.exe
"""

def run():
    while True:
        for proc in psutil.process_iter():
            # print(proc)
            name = proc.name().strip()
            if name == "javaw.exe":
                if ".tlauncher" in proc.exe():
                    print(f"Killing {name}")
                    try:
                        proc.kill()
                    except psutil.NoSuchProcess:
                        print("error while killing .tlauncher javaw.exe")
                childrens = proc.children(recursive=True)
                parents = proc.parents()
                print(childrens, parents, sep="\n\n")
            for bannedproc in BASE_BANNED_APPS:
                if name in bannedproc:
                    print(f"Killing {name}")
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
            out = line.decode().rstrip()
            find_app(out)

def find_app(out:bytearray):
    out = out.decode() if type(out) != str else out
    path_start_index = out.find("C:")
    path = out[path_start_index:].strip()
    if ".tlauncher" in path:
        process_id = ""
        i = path_start_index -1
        print("starting getting id")
        while True:
            letter:str = out[i]
            print(f"letter is {letter}")
            if letter in "1234567890":
                process_id += letter
            else:
                break
        print(process_id, len(process_id))
        proc = psutil.Process(int(process_id))
        print(proc)

# https://stackoverflow.com/questions/54827918/get-list-of-running-windows-applications-using-python
# https://www.geeksforgeeks.org/python-get-list-of-running-processes/
# C:\Users\Lab28\AppData\Roaming\.tlauncher\jvms\jre1.8.0_281\bin\javaw.exe

run()