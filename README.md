# GhostMac – MAC Address Changer

GhostMac is a lightweight and functional tool designed for Linux systems to change network interface MAC addresses, generate random MAC addresses, and restore the original MAC address. The project provides both a Command-Line Interface (CLI) and a Text-based User Interface (TUI).

## Features
- **CLI mode** – Manage directly from the command line via `main.py`
- **TUI mode** – Interactive menu via `tui.py`
- Automatic backup of the original MAC address
- Random MAC address generation
- Logging of MAC address changes
- Simple and safe operation

---

## Installation
```bash
# Clone the repository
git clone https://github.com/haczdd/ghostMac.git
cd ghostMac

# Install dependencies
pip install colorama
```

---

## Usage

### 1. CLI version (`main.py`)
```bash
# Change MAC address
sudo python3 main.py -i eth0 -m 00:11:22:33:44:55

# Assign a random MAC address
sudo python3 main.py -i eth0 --random

# Restore the original MAC address
sudo python3 main.py -i eth0 --reset
```

---

### 2. TUI version (`tui.py`)
```bash
sudo python3 tui.py
```
Menu options:
1. Change MAC address (manual or random)
2. Show current MAC address
3. View log file
4. Restore original MAC address
0. Exit

---

## Project Structure
```
ghostMac/
│── main.py           # CLI version
│── tui.py            # Terminal UI version
│── README.md         # Project documentation
└── requirements.txt  # Dependencies
```

---

## Notes
- This tool has been tested only on **Linux** environments.
- `sudo` privileges are required to change the MAC address.
- Changes are logged in `~/.ghostmac/macchanger.log`.
- The original MAC address is backed up in `~/.ghostmac/<interface>_original_mac.txt` or `~/.original_mac.txt`.


