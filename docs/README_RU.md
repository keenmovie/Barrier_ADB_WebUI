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
sudo apt install adb fastboot
```

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🌐 Автонастройка WireGuard

Если телефон не подключен к серверу напрямую по проводу, используйте скрипт автоматической установки WireGuard от [hwdsl2](https://github.com/hwdsl2/wireguard-install):

```bash
wget [https://git.io/wireguard](https://git.io/wireguard) -O wireguard-install.sh && sudo bash wireguard-install.sh
```

---

## ⚙️ Переменные окружения

| Переменная | Описание | По умолчанию | Обязательно |
| :--- | :--- | :---: | :---: |
| `ADMIN_PASSWORD` | Пароль администратора | — | **Да** |
| `WEBADB_PASSWORD` | Пароль для WebADB | — | **Да** |
| `BARRIER_PHONE` | Номер телефона для управления шлагбаумом | — | **Да** |
| `HOST` | IP-адрес сервера | `0.0.0.0` | Нет |
| `PORT` | Порт приложения | `8090` | Нет |

---

## 🚀 Создание скрипта запуска и Systemd

### 1. Скрипт запуска (`start.sh`)

Создайте файл `start.sh` в корне проекта:

```bash
#!/bin/bash
cd "$(dirname "$0")"
exec .venv/bin/python -m coreapp.webapp
```

Сделайте его исполняемым: `chmod +x start.sh`

---

### 2. Настройка службы Systemd

Создайте файл `/etc/systemd/system/barrier-adb-webui.service`. Служба вызывает **исключительно** ваш файл `start.sh`:

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

Команды управления службой:
```bash
sudo systemctl daemon-reload
sudo systemctl enable barrier-adb-webui.service
sudo systemctl start barrier-adb-webui.service
```

---

## 📱 Работа с ADB

### Подключение к устройству
Для подключения к телефону введите IP-адрес вашего телефона в сети:
```bash
adb connect <IP_телефона>:5555
```

> ⚠️ **Примечание (При перезапуске телефона):**
> Если телефон перезагрузился, сетевой режим ADB отключается. 
> 1. Подключите телефон по USB-шнуру к серверу.
> 2. Выполните команду:
>    ```bash
>    adb tcpip 5555
>    ```
> 3. Отключите USB-шнур и повторно подключитесь по сети:
>    ```bash
>    adb connect <IP_телефона>:5555
>    ```

---

## ⚠️ Отказ от ответственности (Disclaimer)

- **AI Notice:** Код проекта создан и оптимизирован с использованием ИИ. Программное обеспечение предоставляется «как есть» (AS IS).
- **Ограничение ответственности:** Проект предназначен исключительно для личного и учебного использования. Автор **не несёт ответственности** за любые последствия использования ПО (звонки, управление устройством, несанкционированный доступ или противоправные действия). Вся ответственность лежит на пользователе. Подробнее см. в [DISCLAIMER.md](../DISCLAIMER.md).