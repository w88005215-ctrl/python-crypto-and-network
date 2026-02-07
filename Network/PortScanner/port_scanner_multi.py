#!/usr/bin/env python3
import argparse
import ipaddress
import socket

def parse_ports(spec: str):
    out = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            a = int(a); b = int(b)
            if a > b:
                a, b = b, a
            out.extend(range(a, b + 1))
        else:
            out.append(int(part))
    return sorted(set(p for p in out if 1 <= p <= 65535))

def expand_targets(spec: str):
    targets = []
    for item in spec.split(","):
        item = item.strip()
        if not item:
            continue
        if "/" in item:
            net = ipaddress.ip_network(item, strict=False)
            targets.extend([str(ip) for ip in net.hosts()])
        else:
            targets.append(item)
    return targets

def scan_tcp(ip: str, port: int, timeout: float) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            return s.connect_ex((ip, port)) == 0
        except OSError:
            return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", default="127.0.0.1,127.0.0.2")
    ap.add_argument("--ports", default="7999-8001")
    ap.add_argument("--timeout", type=float, default=0.3)
    args = ap.parse_args()

    targets = expand_targets(args.targets)  # список целей
    ports = parse_ports(args.ports)

    for ip in targets:  # for с итерацией IP-адреса
        open_ports = []
        for port in ports:
            if scan_tcp(ip, port, args.timeout):
                open_ports.append(port)

        if open_ports:
            print(f"[OPEN] {ip}: {', '.join(map(str, open_ports))}")
        else:
            print(f"[NONE] {ip}")

if __name__ == "__main__":
    main()
