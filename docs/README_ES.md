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

Interfaz web sencilla para gestionar una barrera a través de un dispositivo Android mediante ADB.

---

## 📋 Tabla de contenidos
- [Requisitos previos](#-requisitos-previos)
- [Configuración de WireGuard](#-configuración-de-wireguard)
- [Variables de entorno](#-variables-de-entorno)
- [Script de inicio y Systemd](#-script-de-inicio-y-servicio-systemd)
- [📱 Uso de ADB](#-uso-de-adb)
- [⚠️ Exención de responsabilidad](#️-exención-de-responsabilidad)

---

## 🛠 Requisitos previos

- **Python 3.11+**
- Herramienta `adb` (Android Debug Bridge)
```bash
sudo apt install adb fastboot
```

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🌐 Configuración de WireGuard

Si el teléfono no está conectado directamente por USB, configure un túnel VPN con el script de [hwdsl2](https://github.com/hwdsl2/wireguard-install):

```bash
wget [https://git.io/wireguard](https://git.io/wireguard) -O wireguard-install.sh && sudo bash wireguard-install.sh
```

---

## ⚙️ Variables de entorno

| Variable | Descripción | Predeterminado | Requerido |
| :--- | :--- | :---: | :---: |
| `ADMIN_PASSWORD` | Contraseña de administrador | — | **Sí** |
| `WEBADB_PASSWORD` | Contraseña para WebADB | — | **Sí** |
| `BARRIER_PHONE` | Número de teléfono para la barrera | — | **Sí** |
| `HOST` | Dirección IP del servidor | `0.0.0.0` | No |
| `PORT` | Puerto de la aplicación | `8090` | No |

---

## 🚀 Script de inicio y Servicio Systemd

### 1. Script de inicio (`start.sh`)

Cree `start.sh` en la raíz del proyecto:

```bash
#!/bin/bash
cd "$(dirname "$0")"
exec .venv/bin/python -m coreapp.webapp
```

Hacer ejecutable: `chmod +x start.sh`

---

### 2. Servicio Systemd

Cree `/etc/systemd/system/barrier-adb-webui.service`:

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

Comandos de gestión:
```bash
sudo systemctl daemon-reload
sudo systemctl enable barrier-adb-webui.service
sudo systemctl start barrier-adb-webui.service
```

---

## 📱 Uso de ADB

### Conexión al dispositivo
Conecte al teléfono por red ingresando su IP:
```bash
adb connect <IP_DEL_TELEFONO>:5555
```

> ⚠️ **Nota (Si se reinicia el teléfono):**
> 1. Conecte por USB al servidor.
> 2. Ejecute: `adb tcpip 5555`
> 3. Desconecte el USB y reconecte por red: `adb connect <IP_DEL_TELEFONO>:5555`

---

## ⚠️ Exención de responsabilidad

- **Aviso de IA:** Código creado y optimizado con asistencia de IA. Se proporciona "TAL CUAL".
- **Limitación de responsabilidad:** El autor no asume ninguna responsabilidad por el uso del software (llamadas, control o uso indebido). Ver [DISCLAIMER.md](../DISCLAIMER.md).