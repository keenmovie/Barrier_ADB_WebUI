import os
from dataclasses import dataclass

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@dataclass
class ConfigClass:
    ADMIN_PASSWORD: str = "TypeYourPasswordHere"  # Change this to a secure password
    BARRIER_PHONE: str = "+1234567890"  # Change this to the phone number that will receive the barrier open command

    # Full path to the SQLite database file
    DATABASE_FILE: str = os.path.join(BASE_DIR, "users.db")

    ADB_PATH: str = os.getenv("ADB_PATH", "adb")

    ADB_HOST: str = os.getenv("ADB_HOST", "")
    CALL_DURATION: int = 20  # Increase call duration

    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes

    # Password for WebADB access
    WEBADB_PASSWORD: str = "TypeYourWebADBPasswordHere"  # Change this to a secure password

    # Host and port for the WSGI server. Adjust as needed for domain deployment.
    HOST: str = os.getenv("HOST", "0.0.0.0")
    # Default port 80 (requires root privileges or CAP_NET_BIND_SERVICE capability).
    # Can be overridden with the PORT environment variable.
    PORT: int = int(os.getenv("PORT", "8090"))
    # Domain name for the application (used for generating absolute URLs if needed).
    # Domain name for generating external URLs. Empty by default for local dev.
    DOMAIN: str = os.getenv("DOMAIN", "")
    # Flask SERVER_NAME should only be set in production when a canonical domain is known.
    SERVER_NAME: str | None = (f"{DOMAIN}:{PORT}" if DOMAIN else None)

# Create configuration instance
Config = ConfigClass()
