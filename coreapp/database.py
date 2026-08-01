import sqlite3
import logging
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_tables()

    def create_tables(self):
        """Create required tables and indexes if they do not exist."""
        try:
            with sqlite3.connect(self.db_file, timeout=10) as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='site_users'")
                if cursor.fetchone() is None:
                    cursor.execute('''
                        CREATE TABLE site_users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password_hash TEXT,
                            role TEXT NOT NULL DEFAULT 'user',
                            created_at TIMESTAMP,
                            expiry_date TIMESTAMP NULL,
                            failed_attempts INTEGER DEFAULT 0,
                            locked_until TIMESTAMP NULL,
                            auth_token TEXT NULL
                        )
                    ''')
                else:
                    cursor.execute("PRAGMA table_info(site_users)")
                    cols = [row[1] for row in cursor.fetchall()]
                    for col_def in [
                        ('expiry_date', 'TIMESTAMP NULL'),
                        ('failed_attempts', 'INTEGER DEFAULT 0'),
                        ('locked_until', 'TIMESTAMP NULL'),
                        ('auth_token', 'TEXT NULL')
                    ]:
                        if col_def[0] not in cols:
                            cursor.execute(f'ALTER TABLE site_users ADD COLUMN {col_def[0]} {col_def[1]}')

                cursor.execute("CREATE INDEX IF NOT EXISTS idx_site_users_username ON site_users(username)")
                conn.commit()
        except Exception as e:
            logger.error(f"Error creating tables: {e}")

    # legacy telegram methods removed; barrier access now uses site_users table
    # (if you still need to migrate telegram user data, you can write a script here)

    # ------------------- web site helpers -------------------
    def add_site_user(self, username, password_hash, role='user', days=0):
        """Create or update a web user. If days>0, set expiry_date accordingly."""
        try:
            created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            expiry = None
            if days > 0:
                expiry = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT OR REPLACE INTO site_users (username, password_hash, role, created_at, expiry_date, failed_attempts, locked_until) VALUES (?, ?, ?, ?, ?, 0, NULL)',
                    (username, password_hash, role, created, expiry)
                )
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error in add_site_user: {e}")
            return False

    def get_site_user(self, username):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, username, password_hash, role, expiry_date FROM site_users WHERE username = ?', (username,))
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error in get_site_user: {e}")
            return None

    def get_site_users(self):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, username, role, created_at, expiry_date FROM site_users')
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error in get_site_users: {e}")
            return []

    def get_site_user_by_id(self, user_id):
        """Fetch a user tuple by numeric id, including lockout info."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, username, password_hash, role, expiry_date, failed_attempts, locked_until FROM site_users WHERE id = ?', (user_id,))
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error in get_site_user_by_id: {e}")
            return None

    def get_site_user_by_auth_token(self, token):
        """Find a user by a signed auth token stored in the database."""
        if not token:
            return None
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, username, password_hash, role, expiry_date, auth_token FROM site_users WHERE auth_token IS NOT NULL')
                for row in cursor.fetchall():
                    stored_hash = row[5]
                    if stored_hash and check_password_hash(stored_hash, token):
                        return (row[0], row[1], row[2], row[3], row[4])
                return None
        except Exception as e:
            logger.error(f"Error in get_site_user_by_auth_token: {e}")
            return None

    def set_site_user_auth_token(self, user_id, token):
        """Store a hashed auth token for a user."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                token_hash = generate_password_hash(token) if token else None
                cursor.execute('UPDATE site_users SET auth_token = ? WHERE id = ?', (token_hash, user_id))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error in set_site_user_auth_token: {e}")
            return False

    def clear_site_user_auth_token(self, user_id):
        """Remove the stored auth token for a user."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE site_users SET auth_token = NULL WHERE id = ?', (user_id,))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error in clear_site_user_auth_token: {e}")
            return False

    def delete_site_user(self, user_id):
        """Remove a user by id. Returns True if deleted, False otherwise.

        The "primary" admin account (username 'admin') is considered special and
        will not be removed even if its id is supplied. This provides a safety
        guard in case the route is invoked incorrectly.
        """
        try:
            # check current username to prevent deleting the built-in admin
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT username FROM site_users WHERE id = ?', (user_id,))
                row = cursor.fetchone()
                if not row:
                    return False
                if row[0] == 'admin':
                    logger.warning('Attempt to delete protected admin account (id=%s)', user_id)
                    return False
                cursor.execute('DELETE FROM site_users WHERE id = ?', (user_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error in delete_site_user: {e}")
            return False

    def update_site_user_password(self, user_id, password_hash):
        """Update a user's password hash. Returns True if updated, False otherwise."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE site_users SET password_hash = ? WHERE id = ?', (password_hash, user_id))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error in update_site_user_password: {e}")
            return False

    def clean_expired_site_users(self):
        try:
            current = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM site_users WHERE expiry_date IS NOT NULL AND expiry_date < ?', (current,))
                conn.commit()
        except Exception as e:
            logger.error(f"Error cleaning expired users: {e}")

    # ---------- Account lockout helpers ----------
    def is_account_locked(self, user_id):
        """Return True if the account is currently locked (locked_until in future)."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT locked_until FROM site_users WHERE id = ?', (user_id,))
                row = cursor.fetchone()
                if row and row[0]:
                    locked_until = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                    return locked_until > datetime.now()
                return False
        except Exception as e:
            logger.error(f"Error checking lockout status: {e}")
            return False

    def reset_failed_attempts(self, user_id):
        """Reset failed_attempts counter and clear lockout."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE site_users SET failed_attempts = 0, locked_until = NULL WHERE id = ?', (user_id,))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error resetting failed attempts: {e}")
            return False

    def increment_failed_attempts(self, user_id, max_attempts: int = 5, lock_minutes: int = 5):
        """Increment failed login attempts and lock the account if limit exceeded.

        Args:
            user_id: ID of the user in ``site_users``.
            max_attempts: Number of allowed failed attempts before lockout.
            lock_minutes: Duration of lockout in minutes.
        Returns:
            ``True`` if the operation succeeded, ``False`` otherwise.
        """
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                # Get current count
                cursor.execute('SELECT failed_attempts FROM site_users WHERE id = ?', (user_id,))
                row = cursor.fetchone()
                current = row[0] if row else 0
                new_count = current + 1
                locked_until = None
                if new_count >= max_attempts:
                    # Set lockout timestamp
                    lock_time = datetime.now() + timedelta(minutes=lock_minutes)
                    locked_until = lock_time.strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(
                    'UPDATE site_users SET failed_attempts = ?, locked_until = ? WHERE id = ?',
                    (new_count, locked_until, user_id)
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error incrementing failed attempts for user {user_id}: {e}")
            return False


