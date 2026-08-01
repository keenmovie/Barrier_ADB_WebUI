<p align="center">
  <b>🇬🇧 English</b> •
  <a href="docs/README_RU.md">🇷🇺 Русский</a> •
  <a href="docs/README_ES.md">🇪🇸 Español</a> •
  <a href="docs/README_FR.md">🇫🇷 Français</a> •
  <a href="docs/README_DE.md">🇩🇪 Deutsch</a>
</p>

# 🚪 Barrier ADB WebUI

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://developer.android.com/tools/adb"><img src="https://img.shields.io/badge/Android_ADB-3DDC84?style=for-the-badge&logo=android&logoColor=white" alt="Android ADB"></a>
  <a href="https://www.wireguard.com/"><img src="https://img.shields.io/badge/WireGuard-88171A?style=for-the-badge&logo=wireguard&logoColor=white" alt="WireGuard"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge" alt="License GPLv3"></a>
</p>

A simple and convenient web interface for controlling a parking barrier via an Android device using the ADB protocol.

---

## 📥 Download Source Code

You can download the latest version directly as a ZIP archive or clone it using Git:

- [📦 **Download ZIP Archive**](https://github.com/keenmovie/Barrier_ADB_WebUI/archive/refs/heads/main.zip)
- **Git Clone:**
  ```bash
  git clone https://github.com/keenmovie/Barrier_ADB_WebUI.git
  ```

---

## 📋 Table of Contents
- [Prerequisites](#-prerequisites)
- [WireGuard Auto-Setup](#-wireguard-auto-setup)
- [Environment Variables](#-environment-variables)
- [Startup Script & Systemd](#-startup-script--systemd-service)
- [📱 ADB Usage](#-adb-usage)
- [⚠️ Legal Disclaimer](#️-legal-disclaimer)

---

## 🛠 Prerequisites

- **Python 3.11+**
- `adb` (Android Debug Bridge) utility

Install system dependencies:
```bash
sudo apt update && sudo apt install -y adb fastboot
```

Setup Virtual Environment & Install requirements:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🌐 WireGuard Auto-Setup

If the phone is not directly connected to the server via USB cable, use the automated WireGuard setup script by [hwdsl2](https://github.com/hwdsl2/wireguard-install):

```bash
wget [https://git.io/wireguard](https://git.io/wireguard) -O wireguard-install.sh && sudo bash wireguard-install.sh
```

---

## ⚙️ Environment Variables

| Variable | Description | Default | Required |
| :--- | :--- | :---: | :---: |
| `ADMIN_PASSWORD` | Administrator password | — | **Yes** |
| `WEBADB_PASSWORD` | Password for WebADB | — | **Yes** |
| `BARRIER_PHONE` | Phone number to control the barrier | — | **Yes** |
| `HOST` | Server IP address | `0.0.0.0` | No |
| `PORT` | Application port | `8090` | No |

---

## 🚀 Startup Script & Systemd Service

### 1. Startup Script (`start.sh`)

Create `start.sh` in the project root:

```bash
#!/bin/bash
cd "$(dirname "$0")"
exec .venv/bin/python -m coreapp.webapp
```

Make it executable:
```bash
chmod +x start.sh
```

---

### 2. Systemd Service Setup

Create `/etc/systemd/system/barrier-adb-webui.service`:

```ini
[Unit]
Description=Barrier ADB WebUI Service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/youdirectory/barrier-adb-webui
ExecStart=/youdirectory/barrier-adb-webui/start.sh
Restart=on-failure
LimitNOFILE=4096

[Install]
WantedBy=multi-user.target
```

Service management commands:
```bash
sudo systemctl daemon-reload
sudo systemctl enable barrier-adb-webui.service
sudo systemctl start barrier-adb-webui.service
```

---

## 📱 ADB Usage

### Connecting to Device
To connect to your phone over the network, enter its IP address:
```bash
adb connect <PHONE_IP>:5555
```

> ⚠️ **Note (When phone reboots):**
> If the phone reboots, network ADB mode is disabled.
> 1. Connect the phone to the server via USB cable.
> 2. Run: `adb tcpip 5555`
> 3. Disconnect the USB cable and reconnect over network: `adb connect <PHONE_IP>:5555`

---

## ⚠️ Legal Disclaimer

- **AI Notice:** The codebase was generated and optimized with AI assistance. The software is provided "AS IS".
- **Limitation of Liability:** This project is intended solely for personal and educational use. The author accepts no liability for any consequences arising from software usage. See [DISCLAIMER.md](DISCLAIMER.md) for full details.

---

## 💖 Support the Project / Поддержать проект

If this project helped you, you can support its development:  
Если проект оказался вам полезен, вы можете поддержать автора:

- [☕ **DonationAlerts** (Карты РФ / СНГ)](https://www.donationalerts.com/r/keenmovie)
- 💎 **USDT (TRC-20):** `TTq5LFaCfJiptzPimcJqhADq7HphJn5gzp`

Thank you for your support! / Спасибо за вашу поддержку!
