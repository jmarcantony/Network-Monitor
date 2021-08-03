import subprocess
import datetime
import json
import time
import sys
import os
import re
try:
    from playsound import playsound
except ModuleNotFoundError:
    print(f"[-] Requirements not satisfied\n\trun {'pip' if os.name == 'nt' else 'pip3'} install -r requirements.txt")
    quit()

CONFIG_FILE_PATH = "network_monitor_config.json"
HOSTS_TO_MONITOR = {}
DELAY = 5

def create_config(wipe_data=False):
    if CONFIG_FILE_PATH not in os.listdir() or wipe_data:
        with open(CONFIG_FILE_PATH, "w") as f:
            f.write("""
{
    "delay": 5,
    "hosts_to_monitor": {}
}
            """)
        print("[+] Succesfully Created Config File")
    else:
        wipe = True if input("[*] Config File Already Exists, Do you want to wipe the data and create a new one (y)es / (n)o: ").lower() == "y" else False
        if wipe:
            create_config(wipe_data=True)

def play_ringtone(path):
    print(f"[*] Playing Ringtone '{path}'")
    try:
        playsound(path)
    except:
        print(f"[-] Could Not Play Ringtone '{path}'... Playing System Beep Noise\a")

def load_config():
    global HOSTS_TO_MONITOR
    global DELAY
    with open(CONFIG_FILE_PATH) as f:
        data = json.load(f)
    try:
        delay = data["delay"]
        hosts = {}
        if not data["hosts_to_monitor"]:
            return True
        for host in data["hosts_to_monitor"]:
            if "ringtone" in data["hosts_to_monitor"][host] and "ring_on_leave" in data["hosts_to_monitor"][host]:
                if host in hosts:
                    print("[-] Config Files Are Corrupted (Repitition Of Host Adresses)... Using Default Mode")
                    return False
                hosts[host] = data["hosts_to_monitor"][host]
            else:
                print("[-] Config Files Are Corrupted (Missing Required Keys For Host Adressess)... Using Default Mode")
                return False
    except Exception as e:
        print("[-] Config Files Are Corrupted (Error In Loading Config File)... Using Default Mode")
        print(f"Error:\n{e}")
        return False
    else:
        HOSTS_TO_MONITOR = hosts
        DELAY = delay
    return True

def get_hosts():
    cmd = "nmap -sP 192.168.0.0/24"
    executed_object = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    executed_data = executed_object.stdout.read() + executed_object.stderr.read()
    raw_data = executed_data.decode()
    return raw_data

def online_hosts(data):
    ip_pattern = r"192.168.[0|1].\d{3}"
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

    print(f"Initial Online Hosts ({datetime.date.today().strftime('%b-%d-%Y')}, {datetime.datetime.now().strftime('%H:%M:%S')}):")
    for host in host_info:
        print(f"{host}: {host_info[host]}")

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
                if host in HOSTS_TO_MONITOR:
                    ringtone = HOSTS_TO_MONITOR[host]["ringtone"]
                    play_ringtone(ringtone)
                changed = True
    
        for host in hosts:
            if host not in curr_hosts:
                print(f"[*] {host_info[host]} ({host}) left the network!")
                if host in HOSTS_TO_MONITOR:
                    if HOSTS_TO_MONITOR[host]["ring_on_leave"]:
                        ringtone = HOSTS_TO_MONITOR[host]
                        play_ringtone(ringtone)
                changed = True
    
        online, hosts = curr_online, curr_hosts
        host_info = curr_host_info
        if not changed:
            print("[*] No change in network so far...")

        print("[*] Sleeping")
        time.sleep(DELAY)

if __name__ == "__main__":
    if "--create-config" in sys.argv and len(sys.argv) == 2:
        create_config()
        quit()

    if not nmap_exists():
        print("[-] This script can only run with nmap installed")
        quit()

    try:
        start = time.time()
        if CONFIG_FILE_PATH in os.listdir():
            success = load_config()
            print(f"\n[*] Successfully Loaded Config Data: {success}\n")
        else:
            print(f"\n[*] Config File Not Found... Using Default Mode\n")
        main()
    except KeyboardInterrupt:
        end = time.time()
        print(f"\n[*] Network Monitored for {round(end - start, 2)}s\n")
        quit()
