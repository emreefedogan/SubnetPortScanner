import socket
import ipaddress
import concurrent.futures
from colorama import Fore, Style

subnet = "193.x.x.0/24"
start_port = 1
end_port = 6500

def scan_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.1)
        result = sock.connect_ex((str(ip), port))
        if result == 0:
            return port
        else:
            return None

def scan_ports(ip):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}
        for future in concurrent.futures.as_completed(futures):
            port = futures[future]
            if (result := future.result()) is not None:
                open_ports.append(result)
    if open_ports:
        result_str = f"{ip} -> {open_ports}\n"
        with open('output.txt', 'a') as file:
            file.write(result_str)
        print(f"{ip} -> {Fore.GREEN}{open_ports}{Style.RESET_ALL}")

if __name__ == "__main__":
    for ip in ipaddress.IPv4Network(subnet):
        scan_ports(ip)
