<p align="center">
  <a href="README.md">🇷🇺 Русский</a> •
  <a href="docs/README_EN.md">🇬🇧 English</a> •
  <a href="docs/README_ES.md">🇪🇸 Español</a> •
  <a href="docs/README_FR.md">🇫🇷 Français</a> •
  <a href="docs/README_DE.md">🇩🇪 Deutsch</a>
</p>

# 🚪 Barrier ADB WebUI

<p align="center">
  <img src="[https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)" alt="Python">
  <img src="[https://img.shields.io/badge/Android_ADB-3DDC84?style=for-the-badge&logo=android&logoColor=white](https://img.shields.io/badge/Android_ADB-3DDC84?style=for-the-badge&logo=android&logoColor=white)" alt="Android ADB">
  <img src="[https://img.shields.io/badge/WireGuard-88171A?style=for-the-badge&logo=wireguard&logoColor=white](https://img.shields.io/badge/WireGuard-88171A?style=for-the-badge&logo=wireguard&logoColor=white)" alt="WireGuard">
  <img src="[https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge](https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge)" alt="License GPLv3">
</p>

Простой и удобный веб-интерфейс для управления шлагбаумом через Android-устройство по протоколу ADB.

---

## 📋 Содержание
- [Предварительные требования](#-предварительные-требования)
- [Автонастройка WireGuard](#-автонастройка-wireguard)
- [Переменные окружения](#-переменные-окружения)
- [Создание скрипта запуска и Systemd](#-создание-скрипта-запуска-и-systemd)
- [📱 Работа с ADB](#-работа-с-adb)
- [⚠️ Отказ от ответственности](#️-отказ-от-ответственности-disclaimer)

---

## 🛠 Предварительные требования

- **Python 3.11+**
- Утилита `adb` (Android Debug Bridge)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt