import os
import subprocess
import time
import logging
from datetime import datetime
from shutil import which
from .config import Config

logger = logging.getLogger(__name__)

class ADBController:
    def __init__(self, adb_path: str = None):
        """Create the controller.
        ``adb_path`` may be ``None`` – in that case we read the value from
        ``Config.ADB_PATH``.  If the resulting path does not point to an existing
        executable we try to resolve it via ``shutil.which`` and, on Windows, we
        also look in the typical Android SDK locations (``%ANDROID_HOME%`` and
        ``%LOCALAPPDATA%\Android\Sdk``).  This makes the controller work out of
        the box on both Linux and Windows development machines.
        """
        # Store the raw path from config or argument
        raw_path = adb_path or Config.ADB_PATH
        # Resolve via which if it is not an absolute file
        if not os.path.isabs(raw_path) and not os.path.isfile(raw_path):
            resolved = which(raw_path)
            if resolved:
                raw_path = resolved
        # Windows‑specific fallback locations (common SDK install paths)
        if os.name == "nt" and not os.path.isfile(raw_path):
            possible = []
            android_home = os.getenv('ANDROID_HOME')
            if android_home:
                possible.append(os.path.join(android_home, 'platform-tools', 'adb.exe'))
            local_app = os.getenv('LOCALAPPDATA')
            if local_app:
                possible.append(os.path.join(local_app, 'Android', 'Sdk', 'platform-tools', 'adb.exe'))
            # Additional hard‑coded defaults that cover most Windows installations
            possible.append(r"C:\Program Files\Android\platform-tools\adb.exe")
            possible.append(r"C:\Program Files (x86)\Android\android-sdk\platform-tools\adb.exe")
            for p in possible:
                if os.path.isfile(p):
                    raw_path = p
                    break
        self.adb_path = raw_path
        self.device_id = None
        self.last_connection_check = None

    # ---------------------------------------------------------------------
    # Permission handling helpers
    # ---------------------------------------------------------------------
    def _grant_call_permission(self, package: str = "com.android.dialer") -> bool:
        """Attempt to grant ``android.permission.CALL_PHONE`` to *package*.
        Returns ``True`` if the ``pm grant`` command succeeded, ``False`` otherwise.
        Some devices use ``com.android.phone`` as the system dialer, others
        ``com.android.dialer``. The method will try the supplied *package* and,
        if it fails, will also try the alternative known dialer package.
        """
        packages_to_try = [package, "com.android.phone"]
        for pkg in packages_to_try:
            try:
                grant_cmd = [
                    self.adb_path,
                    "-s",
                    self.device_id,
                    "shell",
                    "pm",
                    "grant",
                    pkg,
                    "android.permission.CALL_PHONE",
                ]
                logger.info(f"Granting CALL_PHONE permission to {pkg}: {' '.join(grant_cmd)}")
                result = subprocess.run(grant_cmd, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    logger.info(f"Permission CALL_PHONE granted to {pkg}")
                    return True
                else:
                    logger.warning(f"Failed to grant CALL_PHONE to {pkg}: {result.stderr.strip()}")
            except Exception as e:
                logger.error(f"Error granting CALL_PHONE to {pkg}: {e}")
        # If we reach here, none of the attempts succeeded.
        return False


    def _ensure_connected(self):
        """Make sure we have a device ID; attempt connection if not."""
        if not self.device_id:
            return self._connect_device()
        return True

    def _get_available_devices(self):
        """Return a list of currently connected ADB device IDs."""
        try:
            if not os.path.isfile(self.adb_path):
                resolved = which(self.adb_path)
                if resolved:
                    self.adb_path = resolved
            if not os.path.isfile(self.adb_path):
                return []
            result = subprocess.run([self.adb_path, "devices"], capture_output=True, text=True, timeout=10)
            devices = []
            for line in result.stdout.strip().splitlines()[1:]:
                if '\tdevice' in line:
                    devices.append(line.split('\t')[0])
            return devices
        except Exception as e:
            logger.error(f"Error listing ADB devices: {e}")
            return []

    def ensure_device_connected(self, force=False, max_age_seconds: int = 600):
        """Ensure an ADB device is connected, refreshing every 10 minutes by default."""
        now = datetime.now()
        if not force and self.last_connection_check:
            if (now - self.last_connection_check).total_seconds() < max_age_seconds:
                return bool(self.device_id), False

        self.last_connection_check = now
        available_devices = self._get_available_devices()
        if self.device_id and self.device_id in available_devices:
            return True, False

        if self.device_id and self.device_id not in available_devices:
            self.device_id = None

        connected = self._connect_device()
        return connected, connected

    def _connect_device(self):
        """Connect to the Android device via ADB.
        If ``Config.ADB_HOST`` is set, we attempt a remote TCP connection;
        otherwise we rely on a locally attached USB device.
        Returns ``True`` when a device ID is obtained, ``False`` otherwise.
        """
        try:
            # Resolve adb executable if a plain name was provided
            if not os.path.isfile(self.adb_path):
                resolved = which(self.adb_path)
                if resolved:
                    self.adb_path = resolved
            if not os.path.isfile(self.adb_path):
                logger.error(f"ADB executable not found at {self.adb_path}")
                return False

            # Remote connection (if host provided)
            if Config.ADB_HOST:
                adb_host = Config.ADB_HOST.strip()
                if ':' not in adb_host:
                    adb_host = f"{adb_host}:5555"
                logger.info(f"Connecting to remote ADB host: {adb_host}")
                result = subprocess.run(
                    [self.adb_path, "connect", adb_host],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode != 0 or "unable" in result.stderr.lower():
                    logger.error(f"Failed to connect to {adb_host}: {result.stderr.strip()}")
                    return False
                logger.info(f"Connected to {adb_host}")

            # List devices to obtain the device ID
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            logger.info(f"ADB devices output: {result.stdout}")
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                for line in lines[1:]:
                    if '\tdevice' in line:
                        self.device_id = line.split('\t')[0]
                        logger.info(f"Connected to device: {self.device_id}")
                        return True
            logger.error("No devices found")
            return False
        except Exception as e:
            logger.error(f"Error connecting to device: {e}")
            return False

    def make_call(self, phone_number: str):
        """Place a call to ``phone_number`` using the most reliable method.

        1️⃣ Grant ``CALL_PHONE`` permission to the system dialer (if possible).
        2️⃣ Execute ``android.intent.action.CALL`` – this initiates the call directly
           and does **not** require ``INJECT_EVENTS``.
        3️⃣ If the CALL intent fails, fall back to the low‑level ``service call``
           method (works on many devices but may need root).

        Returns ``True`` when the call was successfully started, ``False`` otherwise.
        """
        try:
            # -------------------------------------------------
            # Ensure we have a connected device
            # -------------------------------------------------
            if not self._ensure_connected():
                logger.error("No device connected")
                return False

            # Normalise phone number
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number

            logger.info(f"Attempting direct CALL intent for {phone_number}")

            # -------------------------------------------------
            # 1️⃣ Grant CALL_PHONE permission (best‑effort)
            # -------------------------------------------------
            self._grant_call_permission()

            # -------------------------------------------------
            # 2️⃣ Direct CALL intent – should place the call immediately
            # -------------------------------------------------
            call_cmd = [
                self.adb_path,
                "-s",
                self.device_id,
                "shell",
                "am",
                "start",
                "-a",
                "android.intent.action.CALL",
                "-d",
                f"tel:{phone_number}"
            ]
            logger.info(f"Executing CALL command: {' '.join(call_cmd)}")
            result = subprocess.run(call_cmd, capture_output=True, text=True, timeout=15)
            output = result.stdout + result.stderr
            logger.info(f"ADB Response (CALL): {output.strip()}")
            if result.returncode == 0:
                logger.info("CALL intent executed successfully – the phone should be ringing")
                return True
            else:
                logger.warning("CALL intent failed – will try low‑level telecom service fallback")

            # -------------------------------------------------
            # 3️⃣ Telecom service fallback (may require root)
            # -------------------------------------------------
            return self.make_call_via_telecom(phone_number)

        except Exception as e:
            logger.error(f"Error in make_call: {e}")
            return False
            # ---------- Strategy 1: Direct CALL intent (most reliable if permission granted) ----------
            # Ensure CALL_PHONE permission is granted to the default dialer before attempting.
            self._grant_call_permission()
            call_cmd = [
                self.adb_path,
                "-s",
                self.device_id,
                "shell",
                "am",
                "start",
                "-a",
                "android.intent.action.CALL",
                "-d",
                f"tel:{phone_number}"
            ]
            logger.info(f"Executing direct CALL command: {' '.join(call_cmd)}")
            result = subprocess.run(call_cmd, capture_output=True, text=True, timeout=15)
            output = result.stdout + result.stderr
            logger.info(f"ADB Response (CALL): {output.strip()}")
            if result.returncode == 0:
                logger.info("Direct CALL intent executed successfully")
                return True
            else:
                logger.warning("Direct CALL intent failed – will try DIAL + CALL button")

            # ---------- Strategy 2: DIAL intent + CALL button ----------
            dial_cmd = [
                self.adb_path,
                "-s",
                self.device_id,
                "shell",
                "am",
                "start",
                "-a",
                "android.intent.action.DIAL",
                "-d",
                f"tel:{phone_number}"
            ]
            logger.info(f"Executing DIAL command: {' '.join(dial_cmd)}")
            result = subprocess.run(dial_cmd, capture_output=True, text=True, timeout=15)
            output = result.stdout + result.stderr
            logger.info(f"ADB Response (DIAL): {output.strip()}")

            if result.returncode == 0:
                logger.info(f"DIAL intent started successfully for {phone_number}")
                # Wait a moment for the dialer UI to appear
                time.sleep(1)
                # Try to send CALL key – may fail on non‑rooted devices
                if self._send_call_button():
                    return True
                else:
                    logger.warning("CALL button injection failed – will try telecom service method")
            else:
                logger.warning(f"DIAL command returned {result.returncode}, falling back to telecom service")

            # ---------- Strategy 3: Telecom service (fallback) ----------
            return self.make_call_via_telecom(phone_number)

        except Exception as e:
            logger.error(f"Error in make_call: {e}")
            return False

    def _send_call_button(self):
        """Send KEYCODE_CALL to initiate the call after DIAL intent opens"""
        try:
            cmd = [
                self.adb_path,
                "-s",
                self.device_id,
                "shell",
                "input",
                "keyevent",
                "KEYCODE_CALL"
            ]
            logger.info(f"Sending CALL button: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                logger.info("CALL button sent successfully")
                return True
            else:
                logger.error(f"Error sending CALL button: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error sending CALL button: {e}")
            return False

    def make_call_via_telecom(self, phone_number: str):
        """Alternative method: Use telecom service directly (may require root)"""
        try:
            if not self._ensure_connected():
                logger.error("No device connected")
                return False

            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number

            logger.info(f"Attempting telecom service call to {phone_number}")
            
            # Use telecom service to make call directly
            cmd = [
                self.adb_path,
                "-s",
                self.device_id,
                "shell",
                "service",
                "call",
                "phone",
                "1",
                "s16",
                phone_number
            ]
            
            logger.info(f"Executing telecom service: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            output = result.stdout + result.stderr
            logger.info(f"Telecom response: {output.strip()}")
            
            if result.returncode == 0:
                logger.info("Telecom service call initiated")
                return True
            else:
                logger.warning(f"Telecom service may have failed: {output}")
                return False
        except Exception as e:
            logger.error(f"Error in telecom call: {e}")
            return False

    def make_call_via_phonecall_app(self, phone_number: str):
        """Alternative method: Use com.android.phone application directly"""
        try:
            if not self._ensure_connected():
                logger.error("No device connected")
                return False

            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number

            logger.info(f"Attempting phone app call to {phone_number}")
            
            # Launch phone dialer with pre-filled number
            cmd = [
                self.adb_path,
                "-s",
                self.device_id,
                "shell",
                "am",
                "start",
                "-a",
                "android.intent.action.VIEW",
                "-d",
                f"tel:{phone_number}",
                "com.android.phone"
            ]
            
            logger.info(f"Executing phone app: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                time.sleep(1)
                # Send CALL key
                return self._send_call_button()
            else:
                logger.warning(f"Phone app launch failed")
                return False
        except Exception as e:
            logger.error(f"Error in phone app call: {e}")
            return False

    def end_call(self):
        try:
            time.sleep(1)  # Give a short pause before finishing
            cmd = [
                self.adb_path,
                "-s",
                self.device_id,
                "shell",
                "input",
                "keyevent",
                "KEYCODE_ENDCALL"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            logger.info("Call end command sent")
            return True
        except Exception as e:
            logger.error(f"Error ending call: {e}")
            return False
