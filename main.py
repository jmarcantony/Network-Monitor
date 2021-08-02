import subprocess
import datetime
import time
import re

def get_hosts():
    cmd = "nmap -sP 192.168.0.0/24"
    executed_object = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    executed_data = executed_object.stdout.read() + executed_object.stderr.read()
    raw_data = executed_data.decode()
    return raw_data

def online_hosts(data):
    ip_pattern = r"192.168.0.\d{3}"
    hosts = re.findall(ip_pattern, data)
    return len(hosts), hosts

def nmap_exists():
    cmd = "nmap --version"
    executed_object = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    executed_data = executed_object.stdout.read() + executed_object.stderr.read()
    raw_data = executed_data.decode()
    return True if "Nmap version" in raw_data else False

def main():
    scanned_results = get_hosts()
    online, hosts = online_hosts(scanned_results)

    host_info = {host: scanned_results[:scanned_results.find(f"({host})")].split()[-1] for host in hosts}

    rounds = 0
    
    while True:
        date = datetime.date.today().strftime("%b-%d-%Y")
        curr_time = datetime.datetime.now().strftime("%H:%M:%S")
        rounds += 1
        changed = False
        print(f"\nRound {rounds} ({date}, {curr_time}):")
        print("[*] Scanning...")
        curr_scanned_results = get_hosts()
        curr_online, curr_hosts = online_hosts(curr_scanned_results)
        print("[*] Scan Complete!")
        curr_host_info = {host: curr_scanned_results[:curr_scanned_results.find(f"({host})")].split()[-1] for host in curr_hosts}
        for host in curr_hosts:
            if host not in hosts:
                print(f"[*] {curr_host_info[host]} ({host}) joined the network!")
                changed = True
    
        for host in hosts:
            if host not in curr_hosts:
                print(f"[*] {host_info[host]} ({host}) left the network!")
                changed = True
    
        online, hosts = curr_online, curr_hosts
        host_info = curr_host_info
        if not changed:
            print("[*] No change in network so far...")
        print("[*] Sleeping")
        time.sleep(5)

if __name__ == "__main__":
    if not nmap_exists():
        print("[-] This script can only run with nmap installed")
        quit()
    try:
        start = time.time()
        main()
    except KeyboardInterrupt:
        end = time.time()
        print(f"\n[*] Network Monitored for {round(end - start, 2)}s\n")
        quit()
