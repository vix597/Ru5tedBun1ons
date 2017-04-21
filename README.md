# Ru5tedBun1ons2.0
My bunions...they're so rusty again again (3.0)!

Host range 172.18.30.0 - 172.18.30.255

4 machines:
* 2 Windows 10
* 1 Windows 7
* 1 Ubuntu 16.something

RDP runs on `3389`. Other stuff runs on other ports. How about you figure that out yourself...
1. Ping scan/Port scan
```
nmap -sn -n -T4 172.18.30.0-255
nmap -sS -n -T4 --top-ports 1000 172.18.30.0-255
```
1. Scan range with nmap and find hosts with 3389. Try the `rdesktop` kali command to log into the hosts
1. On the 1 host without 3389....maybe try to `netcat` to the port for some fun times - I think this is running: https://github.com/vix597/vulny
