#! /usr/bin/env python3

import optparse
import socket
from socket import *
from threading import *
from print_color import print

screenLock = Semaphore(value=1)


def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        # connSkt.send("ViolentPython\r\n")
        results = connSkt.recv(1024)
        screenLock.acquire()
        print("[+] %d/tcp open" % tgtPort, color="blue")
        print("[+] " + str(results), color="p")
    except:
        screenLock.acquire()
        print("[-] %d/tcp closed" % tgtPort, color="red")
    finally:
        screenLock.release()
        connSkt.close()


def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host" % tgtHost)
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print("\n[+] Scan Results for: " + tgtName[0], color="blue")
    except:
        print("\n[+] Scan Results for: " + tgtIP, color="blue")
    setdefaulttimeout(2)
    for tgtPort in tgtPorts:
        print("Scanning port " + tgtPort, color="c")
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()


def main():
    parser = optparse.OptionParser("%prog " + '-H <target host> -p "<target port>"')
    parser.add_option("-H", dest="tgtHost", type="string", help="specify target host")
    parser.add_option(
        "-p",
        dest="tgtPort",
        type="string",
        help='specify target port[s] separated by comma. ex : "21, 22" ',
    )
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(", ")
    if (tgtHost == None) | (tgtPorts[0] == None):
        print("[-] You must specify a target host and port[s].")
        exit(0)
    portScan(tgtHost, tgtPorts)


if __name__ == "__main__":
    main()
