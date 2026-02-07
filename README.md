# python-crypto-and-network — Homework

Выполнены задания:
1. HMAC: SHA256 + имя в сообщении.
2. Multi-target TCP port scanner (несколько целей списком, циклы, for по IP).
3. TCP SYN sniffer (Scapy + BPF фильтр `tcp[tcpflags] == 2`).

Пруфы: папка `evidence/`.

---

## 1) HMAC (SHA256) + name in message

### Run
```bash
python3 Crypto/HMAC/HMAC_server.py
python3 Crypto/HMAC/HMAC_client.py
```

### Client output (evidence/hmac_client.txt)
```text
Server answered: Please provide me a comma-separated message,hmac
Access granted!
```

### Server log snippet (evidence/hmac_server_tail.txt)
```text
```

---

## 2) Multi-target port scanner

### Code
`Network/PortScanner/port_scanner_multi.py`

### Demo
```bash
python3 -m http.server 8000 --bind 127.0.0.1
python3 Network/PortScanner/port_scanner_multi.py --targets "127.0.0.1,127.0.0.2" --ports "7999-8001,8000"
```

### Scanner output (evidence/portscan.txt)
```text
[OPEN] 127.0.0.1: 8000
[NONE] 127.0.0.2
```

### HTTP head (optional) (evidence/http_head_8000.txt)
```text
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.13.11
Date: Sat, 07 Feb 2026 14:44:06 GMT
Content-type: text/html; charset=utf-8
Content-Length: 571
```

---

## 3) TCP SYN sniffer (BPF)

Filter: `tcp[tcpflags] == 2`

### Run
```bash
sudo python3 Network/Sniffer/syn_sniffer.py --iface lo
```

### Demo
```bash
python3 -m http.server 8000 --bind 127.0.0.1
curl -I http://127.0.0.1:8000/ >/dev/null
```

### Captured output snippet (evidence/syn_sniffer.txt)
```text
Ether / IP / TCP 127.0.0.1:55222 > 127.0.0.1:8000 S
Ether / IP / TCP 127.0.0.1:55222 > 127.0.0.1:8000 S
```
