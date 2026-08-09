from . import platform
from . import subprocess

def Ping(host:str) -> bool:
    os = platform.system().lower()
    print(f'Connection Checking to Host [ {host} ] ( Platform: {os.capitalize()} )')
    try:
        if subprocess.run(
            ["ping", "-n", "1", "-w", "1000", host] if os == "windows" else ["ping", "-c", "1", "-W", "1", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ).returncode == 0:
            return True
        return False
    except Exception as e:
        print(f'Ping Error to Host [ {host} ] ( Platform: {os.capitalize()} )')
        return False
