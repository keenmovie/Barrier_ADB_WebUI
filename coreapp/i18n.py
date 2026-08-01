from typing import Dict

# Minimal translations dictionary. Add more keys as needed.
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    'brand': {'en': 'Multi', 'ru': 'Мульти'},
    'hero_title': {'en': 'Web UI for opening the barrier', 'ru': 'Веб-интерфейс для открытия шлагбаума'},
    'open_barrier': {'en': 'Open the barrier', 'ru': 'Открыть шлагбаум'},
    'login': {'en': 'Login', 'ru': 'Войти'},
    'settings': {
        'en': 'Settings', 'ru': 'Настройки',
        'es': 'Configuración', 'fr': 'Paramètres', 'de': 'Einstellungen'
    },
    'theme_settings': {
        'en': 'Theme settings', 'ru': 'Настройки темы',
        'es': 'Ajustes de tema', 'fr': 'Paramètres du thème', 'de': 'Themeinstellungen'
    },
    'theme_settings_hint': {
        'en': 'Choose a theme, mode, colors and labels. The values are saved in the settings file.',
        'ru': 'Выберите тему, режим, цвета и подписи. Значения сохраняются в файле настроек.',
        'es': 'Elija un tema, modo, colores y etiquetas. Los valores se guardan en el archivo de configuración.',
        'fr': 'Choisissez un thème, un mode, des couleurs et des libellés. Les valeurs sont enregistrées dans le fichier de paramètres.',
        'de': 'Wählen Sie ein Design, einen Modus, Farben und Bezeichnungen. Die Werte werden in der Einstellungsdatei gespeichert.'
    },
    'theme': {
        'en': 'Theme', 'ru': 'Тема',
        'es': 'Tema', 'fr': 'Thème', 'de': 'Design'
    },
    'mode': {
        'en': 'Mode', 'ru': 'Режим',
        'es': 'Modo', 'fr': 'Mode', 'de': 'Modus'
    },
    'auto': {
        'en': 'Auto', 'ru': 'Авто',
        'es': 'Auto', 'fr': 'Auto', 'de': 'Auto'
    },
    'day': {
        'en': 'Day', 'ru': 'День',
        'es': 'Día', 'fr': 'Jour', 'de': 'Tag'
    },
    'night': {
        'en': 'Night', 'ru': 'Ночь',
        'es': 'Noche', 'fr': 'Nuit', 'de': 'Nacht'
    },
    'medium': {
        'en': 'Medium', 'ru': 'Средний',
        'es': 'Medio', 'fr': 'Moyen', 'de': 'Mittel'
    },
    'logo_color': {
        'en': 'Logo color', 'ru': 'Цвет логотипа',
        'es': 'Color del logo', 'fr': 'Couleur du logo', 'de': 'Logo-Farbe'
    },
    'button_color': {
        'en': 'Button color', 'ru': 'Цвет кнопки',
        'es': 'Color del botón', 'fr': 'Couleur du bouton', 'de': 'Schaltflächenfarbe'
    },
    'button_text_color': {
        'en': 'Button text color', 'ru': 'Цвет текста кнопки',
        'es': 'Color del texto del botón', 'fr': 'Couleur du texte du bouton', 'de': 'Textfarbe der Schaltfläche'
    },
    'brand_text': {'en': 'Brand text', 'ru': 'Текст бренда'},
    'hero_text': {'en': 'Hero text', 'ru': 'Текст заголовка'},
    'button_text': {'en': 'Button text', 'ru': 'Текст кнопки'},
    'save_settings': {
        'en': 'Save settings', 'ru': 'Сохранить настройки',
        'es': 'Guardar ajustes', 'fr': 'Enregistrer les paramètres', 'de': 'Einstellungen speichern'
    },
    'language': {
        'en': 'Language', 'ru': 'Язык',
        'es': 'Idioma', 'fr': 'Langue', 'de': 'Sprache'
    },
    'select_language': {'en': 'Select language', 'ru': 'Выберите язык'},
    'select_theme': {'en': 'Select theme', 'ru': 'Выберите тему'},
    'select_mode': {'en': 'Select mode', 'ru': 'Выберите режим'},
    'current_settings': {'en': 'Current settings', 'ru': 'Текущие настройки'},
    'press_enter_to_keep': {'en': 'Press Enter to keep the current value.', 'ru': 'Нажмите Enter, чтобы оставить текущее значение.'},
    'logout': {'en': 'Logout', 'ru': 'Выйти'},
    'admin_panel': {'en': 'Admin panel', 'ru': 'Панель администратора'},
    'add_user': {'en': 'Add user', 'ru': 'Добавить пользователя'},
    'adb_commands': {'en': 'ADB commands', 'ru': 'ADB команды'},
    'username': {'en': 'Username', 'ru': 'Имя пользователя'},
    'password': {'en': 'Password', 'ru': 'Пароль'},
    'generate': {'en': 'Generate', 'ru': 'Сгенерировать'},
    'show': {'en': 'Show', 'ru': 'Показать'},
    'hide': {'en': 'Hide', 'ru': 'Скрыть'},
    'copy': {'en': 'Copy credentials', 'ru': 'Копировать данные'},
    'return_to_panel': {'en': 'Return to panel', 'ru': 'Вернуться в панель'},
    'role': {'en': 'Role', 'ru': 'Роль'},
    'validity_period': {'en': 'Validity period (days, 0 - unlimited)', 'ru': 'Период действия (дней, 0 - бессрочно)'},
    'add': {'en': 'Add', 'ru': 'Добавить'},
    'reset_password': {'en': 'Reset password', 'ru': 'Сбросить пароль'},
    'delete': {'en': 'Delete', 'ru': 'Удалить'},
    'protected': {'en': '(protected)', 'ru': '(защищено)'},
    'barrier_wait': {'en': 'The button will be available again in 25 seconds.', 'ru': 'Кнопка будет доступна снова через 25 секунд.'},
    'please_login': {'en': 'Please log in to access barrier control and administration features.', 'ru': 'Пожалуйста, войдите, чтобы получить доступ к управлению шлагбаумом и функциям администрирования.'},
    'enter_adb_command': {'en': 'Enter ADB command', 'ru': 'Введите ADB команду'},
    'login_success': {'en': 'Login successful', 'ru': 'Вход выполнен'},
    'remember_me': {'en': 'Remember me', 'ru': 'Запомнить меня'},
    'clipboard_no_access': {'en': 'Unable to access clipboard. Copy credentials manually.', 'ru': 'Не удалось получить доступ к буферу обмена. Скопируйте данные вручную.'},
    'copied_success': {'en': '✓ Copied!', 'ru': '✓ Скопировано!'},
    'clipboard_copy_error': {'en': 'Unable to copy credentials. Please copy manually.', 'ru': 'Не удалось скопировать данные. Скопируйте вручную.'},
    'manage_users_adb': {'en': 'Manage site users and ADB access from one place.', 'ru': 'Управляйте веб-пользователями и доступом ADB в одном месте.'},
    'web_users': {'en': 'Web-users', 'ru': 'Веб-пользователи'},
    'created': {'en': 'Created', 'ru': 'Создано'},
    'expires': {'en': 'Expires', 'ru': 'Истекает'},
    'actions': {'en': 'Actions', 'ru': 'Действия'},
    'confirm_delete': {'en': 'Are you sure?', 'ru': 'Вы уверены?'},
    'never': {'en': 'never', 'ru': 'никогда'},
    'enter_new_password_help': {'en': 'Enter a new password for this user or use the "Generate" button.', 'ru': 'Введите новый пароль для этого пользователя или используйте кнопку «Сгенерировать».'},
    'run': {'en': 'Run', 'ru': 'Выполнить'},
    'result': {'en': 'Result:', 'ru': 'Результат:'},
    'devices_placeholder': {'en': 'devices', 'ru': 'devices'},
    'copyright': {
        'en': '© Keenmovie. All rights reserved.',
        'ru': '© Keenmovie. Все права защищены.',
        'es': '© Keenmovie. Todos los derechos reservados.',
        'fr': '© Keenmovie. Tous droits réservés.',
        'de': '© Keenmovie. Alle Rechte vorbehalten.'
    },
    'user_not_found': {'en': 'User not found or invalid request.', 'ru': 'Пользователь не найден или неверный запрос.'},
}

SUPPORTED_LANGS = ['en', 'ru', 'es', 'fr', 'de']
DEFAULT_LANG = 'en'


def translate(key: str, lang: str | None) -> str:
    if not key:
        return ''
    lang = (lang or DEFAULT_LANG)[:2]
    entry = TRANSLATIONS.get(key)
    if not entry:
        # fallback: return key with spaces
        return key.replace('_', ' ').capitalize()
    # exact lang match
    if lang in entry:
        return entry[lang]
    # try english
    return entry.get('en', next(iter(entry.values())))
