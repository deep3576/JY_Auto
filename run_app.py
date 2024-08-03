import subprocess
import sys
import threading
import webbrowser
import argparse

from getmac import get_mac_address



def check_mac_address(allowed_mac_address):
    from getmac import get_mac_address
    mac_address = get_mac_address()
    if mac_address in allowed_mac_address:
        print("Allowed MAC address found. Running the application.")
        return True
    else:
        print(f"MAC address {mac_address} is not allowed.")
        return False
    

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8000/")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Flask app with MAC address check.')
    parser.add_argument('--mac', type=str, help='Allowed MAC address')
    parser.add_argument('--add-current', action='store_true', help='Add current machine\'s MAC address to the allowed list')
    args = parser.parse_args()

    default_mac_address = "00:1A:2B:3C:4D:5E"
    allowed_mac_addresses = [default_mac_address]

    if args.mac:
        allowed_mac_addresses.append(args.mac)

    if args.add_current:
        current_mac_address = get_mac_address()
        print(f"Adding current MAC address {current_mac_address} to allowed list.")
        allowed_mac_addresses.append(current_mac_address)
        print( allowed_mac_addresses)


    print( allowed_mac_addresses)
    if check_mac_address(allowed_mac_addresses):
        threading.Timer(1.25, open_browser).start()
        subprocess.run([sys.executable, "-m", "gunicorn", "-w", "4", "-b", "127.0.0.1:8000", "app:app"])
    else:
        print("MAC address check failed. Exiting.")


