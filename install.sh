#!/bin/bash

# Update package list and install dependencies
sudo apt-get update
sudo apt-get install -y aircrack-ng nmap python3-pip

# Install Python dependencies
pip3 install scapy

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment and install Python packages
source venv/bin/activate
pip install -r requirements.txt

echo "Installation complete. To start using the Wi-Fi Hacking Tool, activate the virtual environment with 'source venv/bin/activate' and run 'sudo $(which python3) wifi_hacking.py'."
