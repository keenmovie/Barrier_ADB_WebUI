import json
import os
from typing import Any, Dict

from . import i18n


CUSTOM_TEXTS: Dict[str, Dict[str, str]] = {
    'brand': {
        'en': 'My Gate',
        'ru': 'Мой Шлагбаум',
        'es': 'Mi Puerta',
        'fr': 'Ma Barrière',
        'de': 'Meine Schranke',
    },
    'hero_title': {
        'en': 'My web UI for opening the barrier',
        'ru': 'Мой веб-интерфейс для открытия шлагбаума',
        'es': 'Mi interfaz web para abrir la barrera',
        'fr': 'Ma web UI pour ouvrir la barrière',
        'de': 'Meine Web-UI zum Öffnen der Schranke',
    },
    'button_text': {
        'en': 'Open the barrier',
        'ru': 'Открыть шлагбаум',
        'es': 'Abrir la barrera',
        'fr': 'Ouvrir la barrière',
        'de': 'Schranke öffnen',
    },
}

THEMES: Dict[str, Dict[str, Any]] = {
    'default': {
        'name': 'Default',
        'variants': {
            'day': {
                'color_scheme': 'light',
                'colors': {
                    '--bg-color': '#f3f4f6',
                    '--card-bg': '#ffffff',
                    '--surface-bg': '#f8fafc',
                    '--text-color': '#111827',
                    '--muted-color': '#6b7280',
                    '--border-color': 'rgba(148, 163, 184, 0.25)',
                    '--accent-color': '#0f766e',
                    '--accent-strong': '#064e3b',
                    '--btn-bg': '#0f766e',
                    '--btn-text': '#ffffff',
                    '--shadow-soft': '0 16px 40px rgba(15, 23, 42, 0.08)',
                    '--navbar-bg': 'rgba(255, 255, 255, 0.95)',
                    '--navbar-border': 'rgba(148, 163, 184, 0.15)',
                    '--logo-color': '#0f766e',
                },
            },
            'night': {
                'color_scheme': 'dark',
                'colors': {
                    '--bg-color': '#0f172a',
                    '--card-bg': '#111827',
                    '--surface-bg': '#15233c',
                    '--text-color': '#e2e8f0',
                    '--muted-color': '#94a3b8',
                    '--border-color': 'rgba(148, 163, 184, 0.2)',
                    '--accent-color': '#38bdf8',
                    '--accent-strong': '#0ea5e9',
                    '--btn-bg': '#38bdf8',
                    '--btn-text': '#0f172a',
                    '--shadow-soft': '0 16px 40px rgba(15, 23, 42, 0.45)',
                    '--navbar-bg': 'rgba(15, 23, 42, 0.92)',
                    '--navbar-border': 'rgba(148, 163, 184, 0.16)',
                    '--logo-color': '#38bdf8',
                },
            },
            'medium': {
                'color_scheme': 'dark',
                'colors': {
                    '--bg-color': '#e2e8f0',
                    '--card-bg': '#f8fafc',
                    '--surface-bg': '#eef2ff',
                    '--text-color': '#111827',
                    '--muted-color': '#475569',
                    '--border-color': 'rgba(15, 118, 110, 0.2)',
                    '--accent-color': '#2563eb',
                    '--accent-strong': '#1d4ed8',
                    '--btn-bg': '#2563eb',
                    '--btn-text': '#ffffff',
                    '--shadow-soft': '0 16px 40px rgba(30, 41, 59, 0.12)',
                    '--navbar-bg': 'rgba(248, 250, 252, 0.95)',
                    '--navbar-border': 'rgba(148, 163, 184, 0.18)',
                    '--logo-color': '#2563eb',
                },
            },
        },
    },
    'midnight': {
        'name': 'Midnight',
        'variants': {
            'day': {
                'color_scheme': 'light',
                'colors': {
                    '--bg-color': '#f8fafc',
                    '--card-bg': '#ffffff',
                    '--surface-bg': '#eef2ff',
                    '--text-color': '#0f172a',
                    '--muted-color': '#475569',
                    '--border-color': 'rgba(99, 102, 241, 0.2)',
                    '--accent-color': '#4f46e5',
                    '--accent-strong': '#3730a3',
                    '--btn-bg': '#4f46e5',
                    '--btn-text': '#ffffff',
                    '--shadow-soft': '0 16px 40px rgba(15, 23, 42, 0.09)',
                    '--navbar-bg': 'rgba(255, 255, 255, 0.95)',
                    '--navbar-border': 'rgba(99, 102, 241, 0.18)',
                    '--logo-color': '#4f46e5',
                },
            },
            'night': {
                'color_scheme': 'dark',
                'colors': {
                    '--bg-color': '#020617',
                    '--card-bg': '#0f172a',
                    '--surface-bg': '#111c34',
                    '--text-color': '#e2e8f0',
                    '--muted-color': '#94a3b8',
                    '--border-color': 'rgba(148, 163, 184, 0.2)',
                    '--accent-color': '#38bdf8',
                    '--accent-strong': '#0ea5e9',
                    '--btn-bg': '#38bdf8',
                    '--btn-text': '#082f49',
                    '--shadow-soft': '0 16px 40px rgba(2, 6, 23, 0.55)',
                    '--navbar-bg': 'rgba(15, 23, 42, 0.94)',
                    '--navbar-border': 'rgba(148, 163, 184, 0.16)',
                    '--logo-color': '#38bdf8',
                },
            },
            'medium': {
                'color_scheme': 'dark',
                'colors': {
                    '--bg-color': '#0b1120',
                    '--card-bg': '#111827',
                    '--surface-bg': '#1e293b',
                    '--text-color': '#f8fafc',
                    '--muted-color': '#cbd5e1',
                    '--border-color': 'rgba(129, 140, 248, 0.2)',
                    '--accent-color': '#818cf8',
                    '--accent-strong': '#6366f1',
                    '--btn-bg': '#818cf8',
                    '--btn-text': '#0f172a',
                    '--shadow-soft': '0 16px 40px rgba(2, 6, 23, 0.45)',
                    '--navbar-bg': 'rgba(17, 24, 39, 0.93)',
                    '--navbar-border': 'rgba(129, 140, 248, 0.18)',
                    '--logo-color': '#818cf8',
                },
            },
        },
    },
    'forest': {
        'name': 'Forest',
        'variants': {
            'day': {
                'color_scheme': 'light',
                'colors': {
                    '--bg-color': '#f0fdf4',
                    '--card-bg': '#ffffff',
                    '--surface-bg': '#ecfdf5',
                    '--text-color': '#052e16',
                    '--muted-color': '#4b5563',
                    '--border-color': 'rgba(34, 197, 94, 0.18)',
                    '--accent-color': '#16a34a',
                    '--accent-strong': '#166534',
                    '--btn-bg': '#16a34a',
                    '--btn-text': '#ffffff',
                    '--shadow-soft': '0 16px 40px rgba(22, 101, 52, 0.09)',
                    '--navbar-bg': 'rgba(255, 255, 255, 0.95)',
                    '--navbar-border': 'rgba(34, 197, 94, 0.18)',
                    '--logo-color': '#16a34a',
                },
            },
            'night': {
                'color_scheme': 'dark',
                'colors': {
                    '--bg-color': '#07130f',
                    '--card-bg': '#10261b',
                    '--surface-bg': '#143124',
                    '--text-color': '#ecfdf5',
                    '--muted-color': '#a7f3d0',
                    '--border-color': 'rgba(74, 222, 128, 0.2)',
                    '--accent-color': '#34d399',
                    '--accent-strong': '#15803d',
                    '--btn-bg': '#16a34a',
                    '--btn-text': '#f0fdf4',
                    '--shadow-soft': '0 16px 40px rgba(5, 46, 22, 0.45)',
                    '--navbar-bg': 'rgba(16, 38, 27, 0.94)',
                    '--navbar-border': 'rgba(74, 222, 128, 0.16)',
                    '--logo-color': '#34d399',
                },
            },
            'medium': {
                'color_scheme': 'dark',
                'colors': {
                    '--bg-color': '#10261b',
                    '--card-bg': '#143124',
                    '--surface-bg': '#1e3a2b',
                    '--text-color': '#ecfdf5',
                    '--muted-color': '#d1fae5',
                    '--border-color': 'rgba(74, 222, 128, 0.2)',
                    '--accent-color': '#4ade80',
                    '--accent-strong': '#22c55e',
                    '--btn-bg': '#4ade80',
                    '--btn-text': '#052e16',
                    '--shadow-soft': '0 16px 40px rgba(5, 46, 22, 0.32)',
                    '--navbar-bg': 'rgba(20, 49, 36, 0.94)',
                    '--navbar-border': 'rgba(74, 222, 128, 0.16)',
                    '--logo-color': '#4ade80',
                },
            },
        },
    },
    'sunset': {
        'name': 'Sunset',
        'variants': {
            'day': {
                'color_scheme': 'light',
                'colors': {
                    '--bg-color': '#fff7ed',
                    '--card-bg': '#ffffff',
                    '--surface-bg': '#ffedd5',
                    '--text-color': '#431407',
                    '--muted-color': '#9a2c2c',
                    '--border-color': 'rgba(249, 115, 22, 0.2)',
                    '--accent-color': '#f97316',
                    '--accent-strong': '#c2410c',
                    '--btn-bg': '#f97316',
                    '--btn-text': '#fff7ed',
                    '--shadow-soft': '0 16px 40px rgba(146, 64, 14, 0.09)',
                    '--navbar-bg': 'rgba(255, 255, 255, 0.95)',
                    '--navbar-border': 'rgba(249, 115, 22, 0.18)',
                    '--logo-color': '#f97316',
                },
            },
            'night': {
                'color_scheme': 'dark',
                'colors': {
                    '--bg-color': '#1f0f1d',
                    '--card-bg': '#2c1424',
                    '--surface-bg': '#3e1f30',
                    '--text-color': '#fff7ed',
                    '--muted-color': '#fdba74',
                    '--border-color': 'rgba(251, 191, 36, 0.2)',
                    '--accent-color': '#f59e0b',
                    '--accent-strong': '#ea580c',
                    '--btn-bg': '#f97316',
                    '--btn-text': '#fff7ed',
                    '--shadow-soft': '0 16px 40px rgba(46, 16, 33, 0.45)',
                    '--navbar-bg': 'rgba(44, 20, 36, 0.94)',
                    '--navbar-border': 'rgba(251, 191, 36, 0.18)',
                    '--logo-color': '#f59e0b',
                },
            },
            'medium': {
                'color_scheme': 'dark',
                'colors': {
                    '--bg-color': '#2b1120',
                    '--card-bg': '#351827',
                    '--surface-bg': '#4a1d2f',
                    '--text-color': '#fff7ed',
                    '--muted-color': '#fed7aa',
                    '--border-color': 'rgba(249, 115, 22, 0.2)',
                    '--accent-color': '#fb923c',
                    '--accent-strong': '#ea580c',
                    '--btn-bg': '#fb923c',
                    '--btn-text': '#1c1917',
                    '--shadow-soft': '0 16px 40px rgba(46, 16, 33, 0.32)',
                    '--navbar-bg': 'rgba(53, 24, 39, 0.94)',
                    '--navbar-border': 'rgba(249, 115, 22, 0.18)',
                    '--logo-color': '#fb923c',
                },
            },
        },
    },
    'ocean': {
        'name': 'Ocean',
        'variants': {
            'day': {
                'color_scheme': 'light',
                'colors': {
                    '--bg-color': '#f0f9ff',
                    '--card-bg': '#ffffff',
                    '--surface-bg': '#e0f2fe',
                    '--text-color': '#082f49',
                    '--muted-color': '#475569',
                    '--border-color': 'rgba(14, 165, 233, 0.2)',
                    '--accent-color': '#0284c7',
                    '--accent-strong': '#0369a1',
                    '--btn-bg': '#0284c7',
                    '--btn-text': '#f8fafc',
                    '--shadow-soft': '0 16px 40px rgba(2, 132, 199, 0.09)',
                    '--navbar-bg': 'rgba(255, 255, 255, 0.95)',
                    '--navbar-border': 'rgba(14, 165, 233, 0.18)',
                    '--logo-color': '#0284c7',
                },
            },
            'night': {
                'color_scheme': 'dark',
                'colors': {
                    '--bg-color': '#071b2b',
                    '--card-bg': '#0f2740',
                    '--surface-bg': '#113a5b',
                    '--text-color': '#e0f2fe',
                    '--muted-color': '#bae6fd',
                    '--border-color': 'rgba(56, 189, 248, 0.2)',
                    '--accent-color': '#38bdf8',
                    '--accent-strong': '#0ea5e9',
                    '--btn-bg': '#0ea5e9',
                    '--btn-text': '#082f49',
                    '--shadow-soft': '0 16px 40px rgba(2, 6, 23, 0.45)',
                    '--navbar-bg': 'rgba(15, 39, 64, 0.94)',
                    '--navbar-border': 'rgba(56, 189, 248, 0.16)',
                    '--logo-color': '#38bdf8',
                },
            },
            'medium': {
                'color_scheme': 'dark',
                'colors': {
                    '--bg-color': '#072d45',
                    '--card-bg': '#0f3c58',
                    '--surface-bg': '#154f72',
                    '--text-color': '#ecfeff',
                    '--muted-color': '#bae6fd',
                    '--border-color': 'rgba(56, 189, 248, 0.2)',
                    '--accent-color': '#22d3ee',
                    '--accent-strong': '#0891b2',
                    '--btn-bg': '#22d3ee',
                    '--btn-text': '#07212b',
                    '--shadow-soft': '0 16px 40px rgba(2, 6, 23, 0.35)',
                    '--navbar-bg': 'rgba(15, 60, 88, 0.94)',
                    '--navbar-border': 'rgba(56, 189, 248, 0.16)',
                    '--logo-color': '#22d3ee',
                },
            },
        },
    },
    'violet': {
        'name': 'Violet',
        'variants': {
            'day': {
                'color_scheme': 'light',
                'colors': {
                    '--bg-color': '#faf5ff',
                    '--card-bg': '#ffffff',
                    '--surface-bg': '#f5f3ff',
                    '--text-color': '#2e1065',
                    '--muted-color': '#6d28d9',
                    '--border-color': 'rgba(139, 92, 246, 0.2)',
                    '--accent-color': '#7c3aed',
                    '--accent-strong': '#5b21b6',
                    '--btn-bg': '#7c3aed',
                    '--btn-text': '#ffffff',
                    '--shadow-soft': '0 16px 40px rgba(91, 33, 182, 0.09)',
                    '--navbar-bg': 'rgba(255, 255, 255, 0.95)',
                    '--navbar-border': 'rgba(139, 92, 246, 0.16)',
                    '--logo-color': '#7c3aed',
                },
            },
            'night': {
                'color_scheme': 'dark',
                'colors': {
                    '--bg-color': '#120621',
                    '--card-bg': '#1f1137',
                    '--surface-bg': '#28174b',
                    '--text-color': '#f5f3ff',
                    '--muted-color': '#ddd6fe',
                    '--border-color': 'rgba(167, 139, 250, 0.2)',
                    '--accent-color': '#a78bfa',
                    '--accent-strong': '#8b5cf6',
                    '--btn-bg': '#8b5cf6',
                    '--btn-text': '#f5f3ff',
                    '--shadow-soft': '0 16px 40px rgba(17, 24, 39, 0.45)',
                    '--navbar-bg': 'rgba(31, 17, 55, 0.94)',
                    '--navbar-border': 'rgba(167, 139, 250, 0.16)',
                    '--logo-color': '#a78bfa',
                },
            },
            'medium': {
                'color_scheme': 'dark',
                'colors': {
                    '--bg-color': '#1d1131',
                    '--card-bg': '#27183f',
                    '--surface-bg': '#33234d',
                    '--text-color': '#f5f3ff',
                    '--muted-color': '#ddd6fe',
                    '--border-color': 'rgba(167, 139, 250, 0.2)',
                    '--accent-color': '#c084fc',
                    '--accent-strong': '#a855f7',
                    '--btn-bg': '#c084fc',
                    '--btn-text': '#1f2937',
                    '--shadow-soft': '0 16px 40px rgba(17, 24, 39, 0.3)',
                    '--navbar-bg': 'rgba(39, 24, 63, 0.94)',
                    '--navbar-border': 'rgba(167, 139, 250, 0.16)',
                    '--logo-color': '#c084fc',
                },
            },
        },
    },
    'mono': {
        'name': 'Mono',
        'variants': {
            'day': {
                'color_scheme': 'light',
                'colors': {
                    '--bg-color': '#ffffff',
                    '--card-bg': '#ffffff',
                    '--surface-bg': '#f3f3f3',
                    '--text-color': '#000000',
                    '--muted-color': '#6b6b6b',
                    '--border-color': 'rgba(0,0,0,0.08)',
                    '--accent-color': '#000000',
                    '--accent-strong': '#000000',
                    '--btn-bg': '#000000',
                    '--btn-text': '#ffffff',
                    '--shadow-soft': '0 8px 20px rgba(0,0,0,0.04)',
                    '--navbar-bg': 'rgba(255,255,255,0.98)',
                    '--navbar-border': 'rgba(0,0,0,0.06)',
                    '--logo-color': '#000000',
                },
            },
            'night': {
                'color_scheme': 'dark',
                'colors': {
                    '--bg-color': '#0b0b0b',
                    '--card-bg': '#141414',
                    '--surface-bg': '#1f1f1f',
                    '--text-color': '#ffffff',
                    '--muted-color': '#bfbfbf',
                    '--border-color': 'rgba(255,255,255,0.06)',
                    '--accent-color': '#ffffff',
                    '--accent-strong': '#ffffff',
                    '--btn-bg': '#ffffff',
                    '--btn-text': '#000000',
                    '--shadow-soft': '0 8px 20px rgba(0,0,0,0.6)',
                    '--navbar-bg': 'rgba(10,10,10,0.95)',
                    '--navbar-border': 'rgba(255,255,255,0.04)',
                    '--logo-color': '#ffffff',
                },
            },
            'medium': {
                'color_scheme': 'light',
                'colors': {
                    '--bg-color': '#f5f5f5',
                    '--card-bg': '#ffffff',
                    '--surface-bg': '#eeeeee',
                    '--text-color': '#0b0b0b',
                    '--muted-color': '#808080',
                    '--border-color': 'rgba(0,0,0,0.08)',
                    '--accent-color': '#333333',
                    '--accent-strong': '#111111',
                    '--btn-bg': '#333333',
                    '--btn-text': '#ffffff',
                    '--shadow-soft': '0 12px 30px rgba(0,0,0,0.06)',
                    '--navbar-bg': 'rgba(249,249,249,0.97)',
                    '--navbar-border': 'rgba(0,0,0,0.06)',
                    '--logo-color': '#333333',
                },
            },
        },
    },
}

DEFAULT_THEME = 'default'
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'ui_settings.json')


def _build_default_localized_texts() -> Dict[str, Dict[str, str]]:
    defaults: Dict[str, Dict[str, str]] = {}
    for lang in i18n.SUPPORTED_LANGS:
        defaults[lang] = {
            'brand_text': CUSTOM_TEXTS['brand'].get(lang, CUSTOM_TEXTS['brand'].get('en', 'My Gate')),
            'hero_text': CUSTOM_TEXTS['hero_title'].get(lang, CUSTOM_TEXTS['hero_title'].get('en', 'My web UI for opening the barrier')),
            'button_text': CUSTOM_TEXTS['button_text'].get(lang, CUSTOM_TEXTS['button_text'].get('en', 'Open the barrier')),
        }
    return defaults


DEFAULT_UI_SETTINGS: Dict[str, Any] = {
    'language': 'en',
    'theme': DEFAULT_THEME,
    'mode': 'auto',
    'logo_color': '#0f766e',
    'button_color': '#0f766e',
    'button_text_color': '#ffffff',
    'brand_text': 'My Gate',
    'hero_text': 'My web UI for opening the barrier',
    'button_text': 'Open the barrier',
    'localized_texts': _build_default_localized_texts(),
}


def get_language_profile(settings: Dict[str, Any], lang: str | None = None) -> Dict[str, str]:
    language = (lang or settings.get('language') or i18n.DEFAULT_LANG or 'en').strip().lower()[:2]
    localized = settings.get('localized_texts')
    if isinstance(localized, dict) and language in localized and isinstance(localized[language], dict):
        return {
            'brand_text': localized[language].get('brand_text', settings.get('brand_text', 'My Gate')),
            'hero_text': localized[language].get('hero_text', settings.get('hero_text', 'My web UI for opening the barrier')),
            'button_text': localized[language].get('button_text', settings.get('button_text', 'Open the barrier')),
        }
    return {
        'brand_text': settings.get('brand_text', 'My Gate'),
        'hero_text': settings.get('hero_text', 'My web UI for opening the barrier'),
        'button_text': settings.get('button_text', 'Open the barrier'),
    }


def normalize_ui_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(DEFAULT_UI_SETTINGS)
    normalized.update({k: v for k, v in settings.items() if k in DEFAULT_UI_SETTINGS or k == 'localized_texts'})

    if 'localized_texts' in settings and isinstance(settings['localized_texts'], dict):
        localized_texts: Dict[str, Dict[str, str]] = {}
        for lang, values in settings['localized_texts'].items():
            if isinstance(lang, str) and isinstance(values, dict):
                localized_texts[lang] = {
                    'brand_text': str(values.get('brand_text', DEFAULT_UI_SETTINGS['brand_text'])),
                    'hero_text': str(values.get('hero_text', DEFAULT_UI_SETTINGS['hero_text'])),
                    'button_text': str(values.get('button_text', DEFAULT_UI_SETTINGS['button_text'])),
                }
        normalized['localized_texts'] = localized_texts
    else:
        normalized['localized_texts'] = dict(DEFAULT_UI_SETTINGS['localized_texts'])

    language = (settings.get('language') or i18n.DEFAULT_LANG or 'en').strip().lower()[:2]
    if language not in normalized['localized_texts']:
        language = i18n.DEFAULT_LANG

    profile = get_language_profile(normalized, language)
    normalized['brand_text'] = profile['brand_text']
    normalized['hero_text'] = profile['hero_text']
    normalized['button_text'] = profile['button_text']
    return normalized


def get_theme(theme_name: str | None = None, mode: str = 'auto', prefers_dark: bool = False) -> Dict[str, Any]:
    theme_key = (theme_name or DEFAULT_THEME).lower()
    theme = THEMES.get(theme_key, THEMES[DEFAULT_THEME])
    variant_key = mode if mode in {'day', 'night', 'medium'} else ('night' if prefers_dark else 'day')
    variant = theme['variants'].get(variant_key, theme['variants']['day'])
    return {
        'name': theme['name'],
        'mode': variant_key,
        'color_scheme': variant['color_scheme'],
        'colors': variant['colors'],
    }


def load_ui_settings(path: str | None = None) -> Dict[str, Any]:
    settings_path = path or SETTINGS_FILE
    if not os.path.exists(settings_path):
        return dict(DEFAULT_UI_SETTINGS)

    try:
        with open(settings_path, 'r', encoding='utf-8') as handle:
            loaded = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_UI_SETTINGS)

    if not isinstance(loaded, dict):
        return dict(DEFAULT_UI_SETTINGS)

    return normalize_ui_settings(loaded)


def save_ui_settings(settings: Dict[str, Any], path: str | None = None) -> Dict[str, Any]:
    settings_path = path or SETTINGS_FILE
    os.makedirs(os.path.dirname(settings_path), exist_ok=True)
    normalized = normalize_ui_settings(settings)
    with open(settings_path, 'w', encoding='utf-8') as handle:
        json.dump(normalized, handle, indent=2, ensure_ascii=False)
        handle.write('\n')
    return normalized
