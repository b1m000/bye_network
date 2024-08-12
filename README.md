# bye_network
With this tool, you can take down the entire LAN/WLAN in two modes:
  - **Anonymous mode**: Uses an algorithm to create fake MAC addresses.
  - **Normal attack**: Uses your MAC address for the attack

Additionally, you can perform a MITM (Man In The Middle) Attack.


Installing 
- python3 -m pip install -r requests.txt

How to use
- chmod +x bye.py
- sudo ./bye.py
```
python3 bye.py <ip-router> <interface> <b or ba or m>

b -> block
ba -> block in anonymous
m -> man in the middle
```
