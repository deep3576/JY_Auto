import subprocess
import sys
import threading
import webbrowser

from app import open_browser

def check_mac_address():
    from getmac import get_mac_address
    allowed_mac_address = "30:35:ad:ae:7d:80"
    mac_address = get_mac_address()
    if mac_address == allowed_mac_address:
        print("Allowed MAC address found. Running the application.")
        return True
    else:
        print(f"MAC address {mac_address} is not allowed.")
        return False
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8000/")

if __name__ == '__main__':
    if check_mac_address():
        threading.Timer(1.25, open_browser).start()
        subprocess.run([sys.executable, "-m", "gunicorn", "-w", "4", "-b", "127.0.0.1:8000", "app:app"])
        
    else:
        print("MAC address check failed. Exiting.")
