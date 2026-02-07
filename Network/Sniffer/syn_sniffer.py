#!/usr/bin/env python3
import argparse
from scapy.all import sniff

BPF = "tcp[tcpflags] == 2"

def handle(pkt):
    print(pkt.summary())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iface", default="lo")
    ap.add_argument("--count", type=int, default=0)
    args = ap.parse_args()
    sniff(
        iface=args.iface,
        filter=BPF,
        prn=handle,
        store=False,
        count=args.count if args.count > 0 else 0,
    )

if __name__ == "__main__":
    main()
