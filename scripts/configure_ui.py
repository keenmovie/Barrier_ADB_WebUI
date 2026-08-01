import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from coreapp.theme_config import THEMES, DEFAULT_THEME, load_ui_settings, save_ui_settings
from coreapp import i18n


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Interactively configure the barrier UI theme, colors, and labels.')
    parser.add_argument('--theme', choices=sorted(THEMES.keys()), help='Theme name')
    parser.add_argument('--mode', choices=['auto', 'day', 'night', 'medium'], help='Theme mode')
    parser.add_argument('--preset', choices=sorted(THEMES.keys()), help='Apply a theme preset quickly')
    parser.add_argument('--logo-color', help='Logo color as hex')
    parser.add_argument('--button-color', help='Button color as hex')
    parser.add_argument('--button-text-color', help='Button text color as hex')
    parser.add_argument('--brand-text', help='Brand/logo text')
    parser.add_argument('--hero-text', help='Hero title text')
    parser.add_argument('--button-text', help='Barrier button text')
    parser.add_argument('--dry-run', action='store_true', help='Show resulting settings but do not save')
    parser.add_argument('--test', action='store_true', help='Alias for --dry-run (test mode)')
    return parser


def validate_hex(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r'#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})', value):
        raise ValueError('Color must be a hex value like #0f766e')
    return value


def prompt_choice(prompt: str, options: list[str], default: str | None = None) -> str:
    while True:
        print(f'\n{prompt}')
        for index, option in enumerate(options, start=1):
            marker = '>' if option == default else ' '
            print(f'  {marker} {index}. {option}')
        print('Type a number or press Enter to keep the current value.')
        raw = input('> ').strip()
        if raw == '' and default is not None:
            return default
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        if raw in options:
            return raw
        print(f'Please choose one of: {", ".join(options)}')


def prompt_text(prompt: str, default: str | None = None) -> str:
    display_default = f' [{default}]' if default is not None else ''
    raw = input(f'{prompt}{display_default}: ').strip()
    return raw if raw else (default or '')


def prompt_language(default: str | None = None) -> str:
    languages = list(i18n.SUPPORTED_LANGS)
    return prompt_choice('Select language', languages, default or 'en')


def prompt_color(prompt: str, default: str | None = None) -> str:
    while True:
        display_default = f' [{default}]' if default is not None else ''
        raw = input(f'{prompt}{display_default}: ').strip()
        value = raw if raw else (default or '')
        try:
            return validate_hex(value)
        except ValueError as exc:
            print(exc)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    current = load_ui_settings()
    use_interactive = not any([
        args.theme,
        args.mode,
        args.logo_color,
        args.button_color,
        args.button_text_color,
        args.brand_text,
        args.hero_text,
        args.button_text,
    ])

    if use_interactive:
        print('Interactive UI configuration')
        print('Press Enter to keep the current value.')

        theme = prompt_choice('Select theme', sorted(THEMES.keys()), current.get('theme', DEFAULT_THEME))
        mode = prompt_choice('Select mode', ['auto', 'day', 'night', 'medium'], current.get('mode', 'auto'))
        logo_color = prompt_color('Logo color', current.get('logo_color', '#0f766e'))
        button_color = prompt_color('Button color', current.get('button_color', '#0f766e'))
        button_text_color = prompt_color('Button text color', current.get('button_text_color', '#ffffff'))

        localized_texts = {}
        for lang in i18n.SUPPORTED_LANGS:
            profile = (current.get('localized_texts') or {}).get(lang, {}) if isinstance(current.get('localized_texts'), dict) else {}
            print(f'\nConfiguring texts for language: {lang}')
            brand_text = prompt_text(
                f'Brand text [{lang}]',
                profile.get('brand_text', current.get('brand_text', 'My Gate')),
            )
            hero_text = prompt_text(
                f'Hero text [{lang}]',
                profile.get('hero_text', current.get('hero_text', 'My web UI for opening the barrier')),
            )
            button_text = prompt_text(
                f'Button text [{lang}]',
                profile.get('button_text', current.get('button_text', 'Open the barrier')),
            )
            localized_texts[lang] = {
                'brand_text': brand_text,
                'hero_text': hero_text,
                'button_text': button_text,
            }

        # Build the final settings dict matching `theme_config.DEFAULT_UI_SETTINGS` keys
        settings = {
            'language': current.get('language', 'en'),
            'theme': theme,
            'mode': mode,
            'logo_color': logo_color,
            'button_color': button_color,
            'button_text_color': button_text_color,
            'brand_text': localized_texts.get(current.get('language', 'en'), {}).get('brand_text', current.get('brand_text', 'My Gate')),
            'hero_text': localized_texts.get(current.get('language', 'en'), {}).get('hero_text', current.get('hero_text', 'My web UI for opening the barrier')),
            'button_text': localized_texts.get(current.get('language', 'en'), {}).get('button_text', current.get('button_text', 'Open the barrier')),
            'localized_texts': localized_texts,
        }
    else:
        localized_texts = dict(current.get('localized_texts', {}))
        # Support quick presets
        if args.preset:
            preset_theme = args.preset
            preset_mode = 'day'
            # choose a reasonable default mode if theme variant exists
            if 'night' in THEMES.get(preset_theme, {}).get('variants', {}):
                preset_mode = 'night'
            settings = {
                'language': current.get('language', 'en'),
                'theme': preset_theme,
                'mode': preset_mode,
                'logo_color': current.get('logo_color', '#0f766e'),
                'button_color': current.get('button_color', '#0f766e'),
                'button_text_color': current.get('button_text_color', '#ffffff'),
                'brand_text': current.get('brand_text', 'My Gate'),
                'hero_text': current.get('hero_text', 'My web UI for opening the barrier'),
                'button_text': current.get('button_text', 'Open the barrier'),
                'localized_texts': localized_texts,
            }
        else:
            settings = {
                'language': current.get('language', 'en'),
                'theme': args.theme or current.get('theme', DEFAULT_THEME),
                'mode': args.mode or current.get('mode', 'auto'),
                'logo_color': current.get('logo_color', '#0f766e'),
                'button_color': current.get('button_color', '#0f766e'),
                'button_text_color': current.get('button_text_color', '#ffffff'),
                'brand_text': current.get('brand_text', 'My Gate'),
                'hero_text': current.get('hero_text', 'My web UI for opening the barrier'),
                'button_text': current.get('button_text', 'Open the barrier'),
                'localized_texts': localized_texts,
            }
        # override from CLI args if provided
        if args.logo_color:
            settings['logo_color'] = validate_hex(args.logo_color)
        if args.button_color:
            settings['button_color'] = validate_hex(args.button_color)
        if args.button_text_color:
            settings['button_text_color'] = validate_hex(args.button_text_color)
        if args.brand_text is not None:
            settings['brand_text'] = args.brand_text
        if args.hero_text is not None:
            settings['hero_text'] = args.hero_text
        if args.button_text is not None:
            settings['button_text'] = args.button_text

    # Show preview and optionally save
    import json as _json
    preview = _json.dumps(settings, ensure_ascii=False, indent=2)
    print('\nPreview of the settings:')
    print(preview)

    is_dry = args.dry_run or args.test
    if is_dry:
        print('\nDry run / test mode: settings not saved.')
    else:
        ok = input('\nSave these settings to ui_settings.json? [y/N]: ').strip().lower()
        if ok == 'y':
            save_ui_settings(settings)
            print('\nUI settings saved to', os.path.join(ROOT, 'coreapp', 'ui_settings.json'))
        else:
            print('\nAborted. No changes were written.')
    print()
    print(f"Language: {settings['language']}")
    print(f"Theme: {settings['theme']}")
    print(f"Mode: {settings['mode']}")
    print(f"Logo color: {settings['logo_color']}")
    print(f"Button color: {settings['button_color']}")
    print(f"Button text color: {settings['button_text_color']}")
    print(f"Brand text: {settings['brand_text']}")
    print(f"Hero text: {settings['hero_text']}")
    print(f"Button text: {settings['button_text']}")


if __name__ == '__main__':
    main()
