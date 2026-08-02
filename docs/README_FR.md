<p align="center">
  <a href="../README.md">🇬🇧 English</a> •
  <a href="README_RU.md">🇷🇺 Русский</a> •
  <a href="README_ES.md">🇪🇸 Español</a> •
  <b>🇫🇷 Français</b> •
  <a href="README_DE.md">🇩🇪 Deutsch</a>
</p>

# 🚪 Barrier ADB WebUI

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://developer.android.com/tools/adb"><img src="https://img.shields.io/badge/Android_ADB-3DDC84?style=for-the-badge&logo=android&logoColor=white" alt="Android ADB"></a>
  <a href="https://www.wireguard.com/"><img src="https://img.shields.io/badge/WireGuard-88171A?style=for-the-badge&logo=wireguard&logoColor=white" alt="WireGuard"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge" alt="License GPLv3"></a>
</p>

Interface web simple pour gérer une barrière via un appareil Android utilisant le protocole ADB.

---

## 📥 Télécharger le code source

Vous pouvez télécharger la dernière version directement sous forme d'archive ZIP ou cloner le dépôt via Git :

- [📦 **Télécharger l'archive ZIP**](https://github.com/keenmovie/Barrier_ADB_WebUI/archive/refs/heads/main.zip)
- **Cloner avec Git :**
  ```bash
  git clone https://github.com/keenmovie/Barrier_ADB_WebUI.git
  ```

---

## 📋 Table des matières
- [Prérequis](#-prérequis)
- [Configuration WireGuard](#-configuration-wireguard)
- [Variables d'environnement](#-variables-denvironnement)
- [Script de démarrage et Systemd](#-script-de-démarrage-et-service-systemd)
- [📱 Utilisation d'ADB](#-utilisation-dadb)
- [⚠️ Avertissement légal](#️-avertissement-légal)

---

## 🛠 Prérequis

- **Python 3.11+**
- Outil `adb` (Android Debug Bridge)

Installer les dépendances système :
```bash
sudo apt update && sudo apt install -y adb fastboot
```

Environnement virtuel et dépendances :
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🌐 Configuration WireGuard

Si le téléphone n'est pas connecté directement par USB, utilisez le script d'installation automatique WireGuard de [hwdsl2](https://github.com/hwdsl2/wireguard-install) :

```bash
wget [https://git.io/wireguard](https://git.io/wireguard) -O wireguard-install.sh && sudo bash wireguard-install.sh
```

---

## ⚙️ Variables d'environnement

| Variable | Description | Par défaut | Requis |
| :--- | :--- | :---: | :---: |
| `ADMIN_PASSWORD` | Mot de passe administrateur | — | **Oui** |
| `WEBADB_PASSWORD` | Mot de passe pour WebADB | — | **Oui** |
| `BARRIER_PHONE` | Numéro de téléphone de la barrière | — | **Oui** |
| `HOST` | Adresse IP du serveur | `0.0.0.0` | Non |
| `PORT` | Port de l'application | `8090` | Non |

---
## Pour modifier les paramètres de l'interface utilisateur, lancez le fichier configure_ui.py dans le dossier /scripts
---

## 🚀 Script de démarrage et Service Systemd

### 1. Script de démarrage (`start.sh`)

Créez `start.sh` à la racine :

```bash
#!/bin/bash
cd "$(dirname "$0")"
exec .venv/bin/python -m coreapp.webapp
```

Rendre exécutable :
```bash
chmod +x start.sh
```

---

### 2. Service Systemd

Créez `/etc/systemd/system/barrier-adb-webui.service` :

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

Commandes de gestion :
```bash
sudo systemctl daemon-reload
sudo systemctl enable barrier-adb-webui.service
sudo systemctl start barrier-adb-webui.service
```

---

## 📱 Utilisation d'ADB

### Connexion à l'appareil
Saisissez l'adresse IP du téléphone :
```bash
adb connect <IP_DU_TELEPHONE>:5555
```

> ⚠️ **Note (En cas de redémarrage) :**
> 1. Connectez en USB au serveur.
> 2. Exécutez : `adb tcpip 5555`
> 3. Déconnectez le câble USB et reconnectez par réseau : `adb connect <IP_DU_TELEPHONE>:5555`

---

## ⚠️ Avertissement légal

- **Notice IA :** Code créé avec l'aide d'une IA. Fourni "EN L'ÉTAT".
- **Limitation de responsabilité :** L'auteur décline toute responsabilité quant à l'utilisation du logiciel. Voir [DISCLAIMER.md](../DISCLAIMER.md).