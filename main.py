import socket
import sys
import colorama
import os
from queue import Queue
import threading
from datetime import datetime
import re

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

clear()

clear_command = 'cls' if os.name == 'nt' else 'clear'
colorama.init(autoreset=True)

def validate_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def get_ip_from_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.error:
        return None

def get_domain_from_ip(ip):
    try:
        domain = socket.gethostbyaddr(ip)[0]
        return domain
    except socket.herror:
        return None

def extract_domain_ip(text):
    url_pattern = re.compile(r'https?://(www\.)?(\w+\.\w+)')
    match = url_pattern.search(text)
    if match:
        return match.group(2)
    return text

print(colorama.Fore.GREEN + "[Port Scanner]: " + colorama.Fore.LIGHTYELLOW_EX + "Type the IP address or domain to scan.")
host_input = input(colorama.Fore.MAGENTA + "root@you:~$ " + colorama.Fore.WHITE)

host = extract_domain_ip(host_input)

resolved_host = host
while not validate_ip(host):
    ip_from_domain = get_ip_from_domain(host)
    if ip_from_domain:
        resolved_host = ip_from_domain
        break
    else:
        os.system(clear_command)
        print(colorama.Fore.GREEN + "[Port Scanner]: " + colorama.Fore.RED + "Please enter a valid IP address or domain.")
        host = input(colorama.Fore.MAGENTA + "root@you:~$ " + colorama.Fore.WHITE)

os.system(clear_command)
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

if resolved_host != host:
    print(colorama.Fore.GREEN + f"Target IP: {colorama.Fore.LIGHTYELLOW_EX}{resolved_host}{colorama.Fore.WHITE} \n{colorama.Fore.GREEN}Domain: {colorama.Fore.LIGHTYELLOW_EX}{host}\n")
else:
    print(colorama.Fore.GREEN + f"Target IP: {colorama.Fore.LIGHTYELLOW_EX}{host}\n")

open_ports = []
print_lock = threading.Lock()

def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        result = s.connect_ex((resolved_host, port))
        if result == 0: 
            with print_lock:
                open_ports.append(port)
                domain_from_ip = get_domain_from_ip(resolved_host)
                if domain_from_ip:
                    print(f"Port {colorama.Fore.YELLOW}{port}{colorama.Fore.WHITE} is {colorama.Fore.GREEN}open{colorama.Fore.WHITE} on {colorama.Fore.YELLOW}{resolved_host}{colorama.Fore.WHITE} / {colorama.Fore.YELLOW}{domain_from_ip}{colorama.Fore.WHITE}\n")
                else:
                    print(f"Port {colorama.Fore.YELLOW}{port}{colorama.Fore.WHITE} is {colorama.Fore.GREEN}open{colorama.Fore.WHITE} on {colorama.Fore.YELLOW}{resolved_host}{colorama.Fore.WHITE}\n")
        s.close()
    except Exception as e:
        pass

queue = Queue()

def get_ports(mode):
    if mode == 1:
        print("\n" + colorama.Fore.GREEN + "[Port Scanner]: " + colorama.Fore.WHITE + "Scanning " + colorama.Fore.LIGHTYELLOW_EX + "1 " + colorama.Fore.WHITE + "to" + colorama.Fore.LIGHTYELLOW_EX + " 1024" + colorama.Fore.WHITE + " ports...\n")
        for port in range(1, 1025):
            queue.put(port)
    elif mode == 2:
        print("\n" + colorama.Fore.GREEN + "[Port Scanner]: " + colorama.Fore.WHITE + "Scanning " + colorama.Fore.LIGHTYELLOW_EX + "1 " + colorama.Fore.WHITE + "to" + colorama.Fore.LIGHTYELLOW_EX + " 65535" + colorama.Fore.WHITE + " ports...\n")
        for port in range(1, 65536):
            queue.put(port)
    elif mode == 3:
        customPortStart = int(input(colorama.Fore.GREEN + "[Port Scanner]: " + colorama.Fore.LIGHTYELLOW_EX + "Enter starting port number: " + colorama.Fore.WHITE + ""))
        customPortEnd = int(input(colorama.Fore.GREEN + "[Port Scanner]: " + colorama.Fore.LIGHTYELLOW_EX + "Enter ending port number: " + colorama.Fore.WHITE + ""))
        print("\n" + colorama.Fore.GREEN + "[Port Scanner]: " + colorama.Fore.LIGHTYELLOW_EX + "Your Custom" + colorama.Fore.WHITE + " port scanning...\n")
        for port in range(customPortStart, customPortEnd + 1):
            queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        scan(port)

def run_scanner(threads, mode):
    get_ports(mode)
    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()

print(colorama.Fore.GREEN + "[Port Scanner]: " + colorama.Fore.LIGHTYELLOW_EX + "Select your scan type: \n")
print(colorama.Fore.WHITE + "[ " + colorama.Fore.GREEN + "1" + colorama.Fore.WHITE + " ] =" + colorama.Fore.WHITE + " " + colorama.Fore.LIGHTYELLOW_EX + "1" + colorama.Fore.WHITE + " to " + colorama.Fore.LIGHTYELLOW_EX + "1024" + colorama.Fore.WHITE + " port scanning")
print(colorama.Fore.WHITE + "[ " + colorama.Fore.GREEN + "2" + colorama.Fore.WHITE + " ] =" + colorama.Fore.WHITE + " " + colorama.Fore.LIGHTYELLOW_EX + "1" + colorama.Fore.WHITE + " to " + colorama.Fore.LIGHTYELLOW_EX + "65535" + colorama.Fore.WHITE + " port scanning")
print(colorama.Fore.WHITE + "[ " + colorama.Fore.GREEN + "3" + colorama.Fore.WHITE + " ] =" + colorama.Fore.WHITE + " " + colorama.Fore.LIGHTYELLOW_EX + "Your Custom" + colorama.Fore.WHITE + " port scanning\n")

mode = input(colorama.Fore.MAGENTA + "root@you:~$ " + colorama.Fore.WHITE)

while mode not in ['1', '2', '3']:
    print(colorama.Fore.GREEN + "[Port Scanner]: " + colorama.Fore.RED + "Invalid option. Please select a valid option (1, 2, or 3).")
    mode = input(colorama.Fore.MAGENTA + "root@you:~$ " + colorama.Fore.WHITE)

mode = int(mode)

os.system(clear_command)
run_scanner(1021, mode)

while True:
    print(colorama.Fore.GREEN + "[Port Scanner]: " + colorama.Fore.LIGHTYELLOW_EX + "Type the IP address or domain to scan, or 'exit' to quit.")
    host_input = input(colorama.Fore.MAGENTA + "root@you:~$ " + colorama.Fore.WHITE)

    if host_input.lower() == 'exit':
        break

    host = extract_domain_ip(host_input)

    resolved_host = host
    while not validate_ip(host):
        ip_from_domain = get_ip_from_domain(host)
        if ip_from_domain:
            resolved_host = ip_from_domain
            break
        else:
            print(colorama.Fore.GREEN + "[Port Scanner]: " + colorama.Fore.RED + "Please enter a valid IP address or domain.")
            host = input(colorama.Fore.MAGENTA + "root@you:~$ " + colorama.Fore.WHITE)
    
    os.system(clear_command)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    if resolved_host != host:
      print(colorama.Fore.GREEN + f"Target IP: {colorama.Fore.LIGHTYELLOW_EX}{resolved_host}{colorama.Fore.WHITE} \n{colorama.Fore.GREEN}Domain: {colorama.Fore.LIGHTYELLOW_EX}{host}")
    else:
      print(colorama.Fore.GREEN + f"Target IP: {colorama.Fore.LIGHTYELLOW_EX}{host}\n")

    open_ports = []

    run_scanner(1021, mode)
