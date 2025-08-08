#!/usr/bin/env python3
import subprocess
import os
import re
import random
import shutil
from colorama import Fore, Style, init

init(autoreset=True)

INTERFACE = "eth0"  # Öz interfeysin buraya yaz
ORIGINAL_MAC_FILE = os.path.expanduser("~/.original_mac.txt")
LOG_FILE = os.path.expanduser("~/.ghostmac/macchanger.log")

def get_current_mac():
    try:
        output = subprocess.check_output(["ifconfig", INTERFACE]).decode()
        mac = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", output)
        return mac.group(0) if mac else None
    except Exception:
        return None

def save_original_mac():
    if not os.path.exists(ORIGINAL_MAC_FILE):
        mac = get_current_mac()
        if mac:
            os.makedirs(os.path.dirname(ORIGINAL_MAC_FILE), exist_ok=True)
            with open(ORIGINAL_MAC_FILE, "w") as f:
                f.write(mac)

def load_original_mac():
    if os.path.exists(ORIGINAL_MAC_FILE):
        with open(ORIGINAL_MAC_FILE, "r") as f:
            return f.read().strip()
    return None

def change_mac(new_mac):
    try:
        old_mac = get_current_mac()
        subprocess.run(["sudo", "ifconfig", INTERFACE, "down"], check=True)
        subprocess.run(["sudo", "ifconfig", INTERFACE, "hw", "ether", new_mac], check=True)
        subprocess.run(["sudo", "ifconfig", INTERFACE, "up"], check=True)
        log_change(INTERFACE, old_mac, new_mac)
        print(Fore.GREEN + f"[✓] MAC ünvanı dəyişdirildi: {new_mac}")
    except subprocess.CalledProcessError:
        print(Fore.RED + "[✗] MAC ünvanı dəyişdirilmədi! Sudo və ya interfeys adı düzgün ola bilər.")

def generate_random_mac():
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(5))

def restore_original_mac():
    original = load_original_mac()
    if original:
        change_mac(original)
        print(Fore.GREEN + f"[✓] MAC ünvanı orijinala qaytarıldı: {original}")
    else:
        print(Fore.RED + "[✗] Orijinal MAC yadda saxlanmayıb!")

def log_change(interface, old_mac, new_mac):
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(f"{interface} | {old_mac} -> {new_mac}\n")
    except Exception:
        pass  # Loglama xətası kritik deyil

# Tool başlığı
def show_banner():
    os.system("clear")
    print("\033[1;36m" + "="*50)
    print(Fore.CYAN + r"""
        GhostMac starting..
          _____ _               _   __  __          _____
         / ____| |             | | |  \/  |   /\   / ____|
        | |  __| |__   ___  ___| |_| \  / |  /  \ | |
        | | |_ | '_ \ / _ \/ __| __| |\/| | / /\ \| |
        | |__| | | | | (_) \__ \ |_| |  | |/ ____ \ |____
         \_____|_| |_|\___/|___/\__|_|  |_/_/    \_\_____ 
   """ + Style.RESET_ALL)
    print("="*50 + "\033[0m")
    print("\033[1;33mYaradıcı:\033[0m Kifayat Hajizada")
    print("\033[1;33mVersiya:\033[0m 1.0")
    print()

def show_menu():
    print(Fore.GREEN + "[1]" + Style.RESET_ALL + " MAC ünvanını dəyiş")
    print(Fore.GREEN + "[2]" + Style.RESET_ALL + " Cari MAC ünvanını göstər")
    print(Fore.GREEN + "[3]" + Style.RESET_ALL + " Log faylını göstər")
    print(Fore.GREEN + "[4]" + Style.RESET_ALL + " Orijinal MAC ünvanına QAYTAR")   # Əlavə edildi
    print(Fore.GREEN + "[0]" + Style.RESET_ALL + " Çıxış")
    print()

def open_new_terminal():
    terminal_list = [
        ["gnome-terminal", "--"],
        ["xfce4-terminal", "--command"],
        ["konsole", "-e"],
        ["xterm", "-e"],
        ["x-terminal-emulator", "-e"]
    ]
    for term in terminal_list:
        if shutil.which(term[0]):
            subprocess.run(term + ["python3", os.path.abspath(__file__)])
            return
    print(Fore.RED + "❌ Uyğun terminal tapılmadı!" + Style.RESET_ALL)

def main():
    save_original_mac()
    while True:
        show_banner()
        current_mac = get_current_mac()
        print(Fore.MAGENTA + f"İnterfeys: {INTERFACE} | Cari MAC: {current_mac if current_mac else 'Tapılmadı'}" + Style.RESET_ALL)
        show_menu()
        choice = input(Fore.CYAN + "Seçiminiz: " + Style.RESET_ALL).strip()

        if choice == "1":
            print(Fore.YELLOW + "\n[1] Random MAC ünvanı ilə dəyiş")
            print("[2] Manual MAC ünvanı ilə dəyiş\n" + Style.RESET_ALL)
            sub_choice = input("Seçiminiz: ").strip()
            if sub_choice == "1":
                new_mac = generate_random_mac()
                change_mac(new_mac)
            elif sub_choice == "2":
                manual_mac = input("Yeni MAC ünvanını daxil edin (XX:XX:XX:XX:XX:XX): ").strip()
                if re.match(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", manual_mac):
                    change_mac(manual_mac)
                else:
                    print(Fore.RED + "[✗] Yanlış MAC ünvanı formatı!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Yanlış seçim!" + Style.RESET_ALL)
            input("\nDavam etmək üçün Enter bas...")

        elif choice == "2":
            current_mac = get_current_mac()
            print(Fore.YELLOW + f"\nCari MAC ünvanı: {current_mac if current_mac else 'Tapılmadı'}" + Style.RESET_ALL)
            input("\nDavam etmək üçün Enter bas...")

        elif choice == "3":
            if os.path.exists(LOG_FILE):
                os.system(f"less {LOG_FILE}")
            else:
                print(Fore.RED + "\nLog faylı tapılmadı." + Style.RESET_ALL)
                input("\nDavam etmək üçün Enter bas...")

        elif choice == "4":
            restore_original_mac()
            input("\nDavam etmək üçün Enter bas...")

        elif choice == "0":
            print(Fore.YELLOW + "Çıxılır..." + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "Yanlış seçim!" + Style.RESET_ALL)
            input("Davam etmək üçün Enter bas...")

if __name__ == "__main__":
    main()
