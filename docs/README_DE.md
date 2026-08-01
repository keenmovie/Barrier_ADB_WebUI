<p align="center">
  <a href="../README.md">🇬🇧 English</a> •
  <a href="README_RU.md">🇷🇺 Русский</a> •
  <a href="README_ES.md">🇪🇸 Español</a> •
  <a href="README_FR.md">🇫🇷 Français</a> •
  <a href="README_DE.md">🇩🇪 Deutsch</a>
</p>

# 🚪 Barrier ADB WebUI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Android_ADB-3DDC84?style=for-the-badge&logo=android&logoColor=white" alt="Android ADB">
  <img src="https://img.shields.io/badge/WireGuard-88171A?style=for-the-badge&logo=wireguard&logoColor=white" alt="WireGuard">
  <img src="https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge" alt="License GPLv3">
</p>

Einfache Weboberfläche zur Steuerung einer Schranke über ein Android-Gerät via ADB.

---

## 📋 Inhaltsverzeichnis
- [Voraussetzungen](#-voraussetzungen)
- [WireGuard-Einrichtung](#-wireguard-einrichtung)
- [Umgebungsvariablen](#-umgebungsvariablen)
- [Startskript & Systemd](#-startskript--systemd-dienst)
- [📱 ADB-Nutzung](#-adb-nutzung)
- [⚠️ Haftungsausschluss](#️-haftungsausschluss)

---

## 🛠 Voraussetzungen

- **Python 3.11+**
- `adb` (Android Debug Bridge) Werkzeug
```bash
sudo apt install adb fastboot
```

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🌐 WireGuard-Einrichtung

Verwenden Sie das automatische WireGuard-Skript von [hwdsl2](https://github.com/hwdsl2/wireguard-install):

```bash
wget [https://git.io/wireguard](https://git.io/wireguard) -O wireguard-install.sh && sudo bash wireguard-install.sh
```

---

## ⚙️ Umgebungsvariablen

| Variable | Beschreibung | Standard | Erforderlich |
| :--- | :--- | :---: | :---: |
| `ADMIN_PASSWORD` | Administrator-Passwort | — | **Ja** |
| `WEBADB_PASSWORD` | Passwort für WebADB | — | **Ja** |
| `BARRIER_PHONE` | Telefonnummer für die Schranke | — | **Ja** |
| `HOST` | Server-IP-Adresse | `0.0.0.0` | Nein |
| `PORT` | Anwendungsport | `8090` | Nein |

---

## 🚀 Startskript & Systemd-Dienst

### 1. Startskript (`start.sh`)

Erstellen Sie `start.sh` im Projektverzeichnis:

```bash
#!/bin/bash
cd "$(dirname "$0")"
exec .venv/bin/python -m coreapp.webapp
```

Ausführbar machen: `chmod +x start.sh`

---

### 2. Systemd-Dienst

Erstellen Sie `/etc/systemd/system/barrier-adb-webui.service`:

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

Verwaltungsbefehle:
```bash
sudo systemctl daemon-reload
sudo systemctl enable barrier-adb-webui.service
sudo systemctl start barrier-adb-webui.service
```

---

## 📱 ADB-Nutzung

### Verbindung zum Gerät
Geben Sie die IP-Adresse des Telefons ein:
```bash
adb connect <TELEFON_IP>:5555
```

> ⚠️ **Hinweis (Bei Neustart des Telefons):**
> 1. Per USB an den Server anschließen.
> 2. Ausführen: `adb tcpip 5555`
> 3. USB-Kabel trennen und erneut über Netzwerk verbinden: `adb connect <TELEFON_IP>:5555`

---

## ⚠️ Haftungsausschluss

- **KI-Hinweis:** Code mit KI-Unterstützung erstellt. Bereitstellung erfolgt "WIE ER IST".
- **Haftungsbeschränkung:** Der Autor übernimmt keine Haftung für die Nutzung der Software. Siehe [DISCLAIMER.md](../DISCLAIMER.md).