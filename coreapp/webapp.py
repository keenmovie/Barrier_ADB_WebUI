import os
import logging
import shlex
from datetime import datetime, timedelta
from flask import (Flask, render_template, redirect, url_for, request, session, flash, g)
from werkzeug.security import generate_password_hash, check_password_hash
from .database import Database
from .config import Config
from .adb_controller import ADBController
from .theme_config import THEMES, DEFAULT_THEME, CUSTOM_TEXTS, get_theme, load_ui_settings, save_ui_settings, get_language_profile

# logging configuration
logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.isdir(logs_dir):
    os.makedirs(logs_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Flask, by default, looks for ``templates`` and ``static`` directories relative to
# the *application root path* (``app.root_path``). To make sure Flask finds the
# correct directories in this package layout, we explicitly pass absolute paths
# for both ``template_folder`` and ``static_folder``.
_base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(_base_dir, 'templates'),
    static_folder=os.path.join(_base_dir, 'static')
)
# Log the resolved template/static paths – helps verify that Flask can locate them.
# Enable CSRF protection globally.
# In production, this should always be enabled for forms that mutate state.
app.config['WTF_CSRF_ENABLED'] = os.environ.get('FLASK_ENV') != 'testing'
# Maximum upload size: 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Apply permanent session lifetime from config (seconds)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=Config.PERMANENT_SESSION_LIFETIME)
# Generate a secret key at runtime for Flask session handling.
# This avoids storing a static SECRET_KEY variable while still satisfying Flask's requirement.
import secrets
app.secret_key = secrets.token_urlsafe(32)
app.config['SECRET_KEY'] = app.secret_key
# Harden session cookie settings
# NOTE: During local development or when the site is accessed via plain HTTP
# (e.g. http://<ip>:8090 or through a reverse proxy that terminates TLS),
# the ``SESSION_COOKIE_SECURE`` flag must be ``False``; otherwise the session
# cookie is marked as *Secure* and the browser will not send it over HTTP.
# In production you should set this back to ``True`` and serve the site over
# HTTPS (e.g. with a Let’s Encrypt certificate installed via win‑acme).
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False  # set to True only when serving over HTTPS
)
# Configure SERVER_NAME for generating absolute URLs (e.g., when using url_for with _external=True).
app.config['SERVER_NAME'] = Config.SERVER_NAME
from flask_wtf import CSRFProtect
from . import i18n
import locale

# Create the CSRFProtect instance and bind it to the Flask app.
csrf = CSRFProtect(app)

# initialize database and ADB controller
db = Database(Config.DATABASE_FILE)
adb = ADBController()

@app.before_request
def detect_user_language():
    settings = load_ui_settings()
    supported = i18n.SUPPORTED_LANGS

    try:
        best = request.accept_languages.best_match(supported)
        if best:
            g.lang = best[:2]
            return
    except Exception:
        pass

    configured_lang = (settings.get('language') or '').strip().lower()[:2]
    if configured_lang in supported:
        g.lang = configured_lang
        return

    try:
        system_locale = locale.getdefaultlocale()[0] or ''
        if system_locale:
            g.lang = system_locale.split('_')[0]
        else:
            g.lang = i18n.DEFAULT_LANG
    except Exception:
        g.lang = i18n.DEFAULT_LANG


# expose a simple translation function to templates
@app.context_processor
def inject_helpers():
    lang = getattr(g, 'lang', None)

    def translate(key: str, default: str | None = None) -> str:
        translated = i18n.translate(key, lang)
        if translated == key.replace('_', ' ').capitalize() and default is not None:
            return default
        return translated

    stored_settings = load_ui_settings()

    theme_name = stored_settings.get('theme', DEFAULT_THEME) or DEFAULT_THEME
    mode = stored_settings.get('mode', 'auto') or 'auto'
    prefers_dark = False
    try:
        # Prefer explicit cookie set by client-side JS, fallback to client hint header.
        cookie_pref = request.cookies.get('prefers_color_scheme', '')
        if cookie_pref:
            prefers_dark = cookie_pref.lower() == 'dark'
        else:
            prefers_dark = request.headers.get('Sec-CH-Prefers-Color-Scheme', '').lower() == 'dark'
    except Exception:
        prefers_dark = False
    theme = get_theme(theme_name, mode=mode, prefers_dark=prefers_dark)
    custom_texts = CUSTOM_TEXTS
    language_profile = get_language_profile(stored_settings, lang)
    stored_settings['brand_text'] = language_profile['brand_text']
    stored_settings['hero_text'] = language_profile['hero_text']
    stored_settings['button_text'] = language_profile['button_text']

    return {
        '_': lambda key: translate(key),
        'theme': theme,
        'theme_name': theme_name,
        'theme_mode': mode,
        'themes': THEMES,
        'custom_text': lambda key: custom_texts.get(key, {}).get(lang, custom_texts.get(key, {}).get('en', '')),
        'site_settings': stored_settings,
        'current_year': datetime.now().year,
    }

# ensure there's at least one admin user for the website
if not db.get_site_user('admin'):
    db.add_site_user('admin', generate_password_hash(Config.ADMIN_PASSWORD), role='admin')
# cleanup expired users on startup
try:
    db.clean_expired_site_users()
except Exception:
    pass

# helpers

def _user_is_active(user):
    if not user:
        return False
    expiry_str = user[4]
    if not expiry_str:
        return True
    try:
        return datetime.strptime(expiry_str, '%Y-%m-%d %H:%M:%S') >= datetime.now()
    except Exception:
        return False


def logged_in():
    """Return True if the current user is authenticated via session or device cookie."""
    if session.get('user_id') is not None:
        user = db.get_site_user_by_id(session['user_id'])
        if not user:
            session.clear()
            return False
        if not _user_is_active(user):
            db.clear_site_user_auth_token(user[0])
            session.clear()
            return False
        return True

    token = request.cookies.get('auth_token')
    if not token:
        return False

    user = db.get_site_user_by_auth_token(token)
    if not user:
        return False
    if not _user_is_active(user):
        db.clear_site_user_auth_token(user[0])
        return False

    session['user_id'] = user[0]
    session['username'] = user[1]
    session['role'] = user[3]
    return True


def is_admin():
    return session.get('role') == 'admin'


@app.route('/')
def index():
    return render_template('index.html', logged_in=logged_in(), admin=is_admin())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if logged_in():
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.get_site_user(username)
        # Check if the account is locked before verifying password
        if user and db.is_account_locked(user[0]):
            flash('Account is locked. Please try again later.', 'danger')
            logger.warning('Locked account login attempt: %s', username)
            return render_template('login.html')
        if user and password and check_password_hash(user[2], password):
            expiry = user[4]
            if expiry and datetime.strptime(expiry, '%Y-%m-%d %H:%M:%S') < datetime.now():
                flash('Access period has expired', 'danger')
                return render_template('login.html')
            # Successful login – reset failed attempts
            db.reset_failed_attempts(user[0])
            session.permanent = True
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            auth_token = secrets.token_urlsafe(32)
            db.set_site_user_auth_token(user[0], auth_token)
            response = redirect(url_for('index'))
            response.set_cookie(
                'auth_token',
                auth_token,
                httponly=True,
                samesite='Lax',
                max_age=60 * 60 * 24 * 30
            )
            flash('Login successful', 'success')
            return response
        else:
            # Increment failed attempts if user exists
            if user:
                db.increment_failed_attempts(user[0])
            flash('Invalid username or password', 'danger')

    return render_template('login.html', logged_in=logged_in(), admin=is_admin())

@app.route('/logout')
def logout():
    # Show a warning flash when the user logs out
    user_id = session.get('user_id')
    if user_id:
        db.clear_site_user_auth_token(user_id)
    session.clear()
    response = redirect(url_for('index'))
    response.set_cookie('auth_token', '', expires=0, httponly=True, samesite='Lax')
    flash('You have been logged out', 'warning')
    return response

# The settings UI is intentionally removed from the web interface. Configuration
# is available via CLI script (scripts/configure_ui.py) and persisted in
# `ui_settings.json`. Keeping the route removed prevents accidental site exposure.

# admin routes
@app.route('/admin')
def admin_panel():
    if not logged_in() or not is_admin():
        return redirect(url_for('login'))
    # remove expired users each time admin visits
    db.clean_expired_site_users()
    users = db.get_site_users()
    return render_template('admin_panel.html', users=users, logged_in=logged_in(), admin=is_admin())

@app.route('/admin/webadb', methods=['GET', 'POST'])
def webadb_access():
    if not logged_in() or not is_admin():
        return redirect(url_for('login'))
    output = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password == Config.WEBADB_PASSWORD:
            command = request.form.get('command', '').strip()
            if command:
                try:
                    import subprocess
                    result = subprocess.run([Config.ADB_PATH] + shlex.split(command), capture_output=True, text=True, timeout=30)
                    output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
                except Exception as e:
                    output = f"Error: {e}"
            else:
                output = "Enter ADB command"
        else:
            flash('Invalid password', 'danger')
    return render_template('webadb.html', logged_in=logged_in(), admin=is_admin(), output=output)

@app.route('/admin/users/add', methods=['GET', 'POST'])
def add_site_user():
    if not logged_in() or not is_admin():
        return redirect(url_for('login'))
    credentials = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'user')
        days = int(request.form.get('days', '0') or 0)
        if not username or not password:
            flash('Username and password are required', 'danger')
            return render_template('add_user.html', logged_in=logged_in(), admin=is_admin(), credentials=credentials)
        hash_pw = generate_password_hash(password)
        db.add_site_user(username, hash_pw, role, days)
        credentials = {'username': username, 'password': password}
    return render_template('add_user.html', logged_in=logged_in(), admin=is_admin(), credentials=credentials)


@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
def delete_site_user(user_id):
    if not logged_in() or not is_admin():
        return redirect(url_for('login'))
    # prevent admin account deletion
    user = db.get_site_user_by_id(user_id) if hasattr(db, 'get_site_user_by_id') else None
    if user and user[1] == 'admin':
        flash('Main admin account cannot be deleted', 'warning')
        logger.warning('Admin tried to delete main admin account %s', user_id)
        return redirect(url_for('admin_panel'))
    if db.delete_site_user(user_id):
        logger.info(f'User {user_id} deleted by admin {session.get("user_id")}')
        flash('User deleted', 'info')
    return redirect(url_for('admin_panel'))

@app.route('/admin/users/reset-password/<int:user_id>', methods=['GET', 'POST'])
def reset_site_user_password(user_id):
    if not logged_in() or not is_admin():
        return redirect(url_for('login'))
    
    user = db.get_site_user_by_id(user_id) if hasattr(db, 'get_site_user_by_id') else None
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin_panel'))
    
    if user[1] == 'admin':
        flash('Cannot change the main admin account password', 'warning')
        logger.warning('Admin tried to reset main admin account password (id=%s)', user_id)
        return redirect(url_for('admin_panel'))
    
    new_password = None
    if request.method == 'POST':
        new_password = request.form.get('password')
        if new_password:
            hash_pw = generate_password_hash(new_password)
            if db.update_site_user_password(user_id, hash_pw):
                credentials = {'username': user[1], 'password': new_password}
                return render_template('reset_password.html', credentials=credentials, logged_in=logged_in(), admin=is_admin())
            else:
                    flash('Error updating password', 'danger')
    
    user = db.get_site_user_by_id(user_id) if hasattr(db, 'get_site_user_by_id') else None
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('admin_panel'))
    
    credentials = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password:
            credentials = {'username': user[1], 'password': password}
    
    return render_template('reset_password.html', user=user, credentials=credentials, logged_in=logged_in(), admin=is_admin())

# barrier control accessible only to admins
@app.route('/barrier', methods=['POST'])
def open_barrier():
    """Execute the ADB call to open the barrier.
    Called via POST from the barrier page.
    """
    if not logged_in():
        flash('Only logged-in users can open the barrier', 'danger')
        return redirect(url_for('login'))

    device_connected, reconnected = adb.ensure_device_connected(force=True)
    if reconnected:
        session.pop('barrier_cooldown_until', None)

    if not device_connected:
        session.pop('barrier_cooldown_until', None)
        flash('ADB device not found. Reconnecting, but barrier cannot be opened now.', 'warning')
        return redirect(url_for('index'))

    cooldown_until = session.get('barrier_cooldown_until')
    if cooldown_until and not reconnected:
        try:
            if datetime.fromisoformat(cooldown_until) > datetime.now():
                flash('Please wait 25 seconds before opening the barrier again', 'warning')
                return redirect(url_for('index'))
        except ValueError:
            pass

    try:
        call_result = adb.make_call(Config.BARRIER_PHONE)
        if call_result:
            session['barrier_cooldown_until'] = (datetime.now() + timedelta(seconds=25)).isoformat()
            flash('Barrier call completed', 'success')
        else:
            flash('Failed to make the call', 'danger')
    except Exception as e:
        logger.error(f'Error opening barrier: {e}')
        flash('Error while trying to open the barrier', 'danger')
    # Return to main page after attempt
    return redirect(url_for('index'))


# Safe import of waitress for static analysis / optional dependency
try:
    from waitress import serve  # type: ignore
except ImportError:  # pragma: no cover
    serve = None  # waitress not available

if __name__ == '__main__':
    # Production entry point using a WSGI server (waitress) when available.
    if serve:
        serve(app, host=Config.HOST, port=Config.PORT)
    else:
        logger.error('waitress not installed – falling back to Flask development server')
        # Use Config host/port for Flask dev server as well.
        app.run(host=Config.HOST, port=Config.PORT)
