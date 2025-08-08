#!/usr/bin/env python3
import subprocess
import argparse
import re
import random
from colorama import Fore, Style, init
import sys
from datetime import datetime
import os

# Init colorama
init(autoreset=True)

# Paths
home = os.path.expanduser("~")
CONFIG_DIR = os.path.join(home, ".ghostmac")
LOG_FILE = os.path.join(CONFIG_DIR, "macchanger.log")

def ensure_config_dir():
    if not os.path.exists(CONFIG_DIR):
        try:
            os.makedirs(CONFIG_DIR)
        except Exception as e:
            print(Fore.RED + f"[✗] Failed to create directory {CONFIG_DIR}: {e}" + Style.RESET_ALL)
            sys.exit(1)

def get_backup_path(interface):
    return os.path.join(CONFIG_DIR, f"{interface}_original_mac.txt")

def log_change(interface, old_mac, new_mac):
    try:
        with open(LOG_FILE, "a") as log:
            log.write(f"{datetime.now()} | {interface} | {old_mac} -> {new_mac}\n")
    except Exception as e:
        print(Fore.RED + f"[✗] Failed to write log: {e}" + Style.RESET_ALL)

def print_banner():
    print(Fore.CYAN + r"""
    GhostMac starting..
      _____ _               _   __  __          _____
     / ____| |             | | |  \/  |   /\   / ____|
    | |  __| |__   ___  ___| |_| \  / |  /  \ | |
    | | |_ | '_ \ / _ \/ __| __| |\/| | / /\ \| |
    | |__| | | | | (_) \__ \ |_| |  | |/ ____ \ |____
     \_____|_| |_|\___/|___/\__|_|  |_/_/    \_\_____ 
                                                     by Kifayat 🚀
    """ + Style.RESET_ALL)

def user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--interface', dest='interface', help='Enter your interface')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-m', '--mac' , dest='mac_address', help="Enter new mac address")
    group.add_argument('--random', action='store_true', help='Generate random MAC address')
    group.add_argument('--reset', action='store_true', help='Reset to original MAC address (if backup exists)')
    return parser.parse_args()

def is_valid_mac(mac):
    pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
    return re.fullmatch(pattern, mac) is not None

def generate_random_mac():
    mac = [0x00, 0x16, 0x3E,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join('%02x' % x for x in mac)

def control_inputs(interface, mac_address, random_flag):
    if not interface:
        interface = input('Enter your interface: ')
    if random_flag:
        mac_address = generate_random_mac()
        print(f"[i] Generated random MAC: {mac_address}")
    elif not mac_address and not random_flag:
        mac_address = input('Enter new mac address: ')
    return interface, mac_address

def control_mac_address(interface):
    try:
        ifconfig = subprocess.check_output(['ifconfig', interface])
        old_mac_address = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(ifconfig))
        if old_mac_address:
            return old_mac_address.group(0)
        else:
            return None
    except subprocess.CalledProcessError:
        print(Fore.RED + f"[✗] Failed to get current MAC of {interface}" + Style.RESET_ALL)
        sys.exit(1)

def mac_changer(interface, mac_address):
    print(f"[*] Trying to change MAC address of {interface} to {mac_address}...")
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', mac_address])
    subprocess.call(['ifconfig', interface, 'up'])

def manage_original_mac(interface):
    """
    Bu funksiya orijinal MAC ünvanının backup faylı varsa oxuyur və qaytarır.
    Backup yoxdursa orijinal MAC-ı tapıb fayla yazır və qaytarır.
    """
    path = get_backup_path(interface)
    if os.path.exists(path):
        with open(path, "r") as f:
            original_mac = f.read().strip()
        return original_mac

    # Backup yoxdursa orijinal MAC-ı oxu
    try:
        with open(f"/sys/class/net/{interface}/address") as f:
            original_mac = f.read().strip()
    except Exception:
        original_mac = None

    if not original_mac or not is_valid_mac(original_mac):
        original_mac = control_mac_address(interface)

    if original_mac and is_valid_mac(original_mac):
        with open(path, "w") as f:
            f.write(original_mac)
        print(Fore.YELLOW + f"[i] Original MAC for {interface} saved: {original_mac}" + Style.RESET_ALL)
        return original_mac
    else:
        print(Fore.RED + "[✗] Could not determine original MAC address" + Style.RESET_ALL)
        sys.exit(1)

# ===== Main proqram =====
args = user_input()
ensure_config_dir()
print_banner()

if args.reset:
    if not args.interface:
        print(Fore.RED + "[✗] Interface is required when using --reset" + Style.RESET_ALL)
        sys.exit(1)
    original_mac = manage_original_mac(args.interface)
    if not original_mac or not is_valid_mac(original_mac):
        print(Fore.RED + f"[✗] No valid original MAC found for {args.interface}" + Style.RESET_ALL)
        sys.exit(1)
    print(f"[*] Resetting {args.interface} to original MAC: {original_mac}")
    mac_changer(args.interface, original_mac)
    sys.exit(0)  # Resetdən sonra proqram bitir

interface, mac_address = control_inputs(args.interface, args.mac_address, args.random)

# Orijinal MAC backup-u yaradılır (əgər yoxdursa)
manage_original_mac(interface)

if not is_valid_mac(mac_address):
    print(Fore.RED + "[✗] Invalid MAC address format! Use format like: 00:11:22:33:44:55" + Style.RESET_ALL)
    sys.exit(1)

mac_changer(interface, mac_address)

finalized_mac = control_mac_address(interface)
if finalized_mac == mac_address:
    print(Fore.GREEN + "[✓] MAC address changed successfully" + Style.RESET_ALL)
    log_change(interface, manage_original_mac(interface), mac_address)
else:
    print(Fore.RED + "[✗] Failed to change MAC" + Style.RESET_ALL)
