from jproperties import Properties
from django.conf import settings
import os

def get_translation(lang: str):
    lang = lang.lower()
    if lang not in ['ru', 'en']:
        lang = 'ru'
    path = settings.BASE_DIR / "cards" / "locale" / lang / "messages.properties"
    if not path.exists():
        print(f"File not found: {path} — fallback to ru")  # Дебаг
        lang = 'ru'
        path = settings.BASE_DIR / "cards" / "locale" / "ru" / "messages.properties"
        if not path.exists():
            print(f"Fallback failed: {path}")
            return {}
    props = Properties()
    with open(path, "rb") as f:
        props.load(f, "utf-8")
    # Flattened result from properties: keys may contain dots (e.g. 'title.list')
    flat = {k: v[0] if isinstance(v, tuple) else v for k, v in props.properties.items()}

    # Convert dotted keys into nested dict so templates can use `t.title.list`
    nested = {}

    def set_nested(d: dict, parts: list, value):
        for part in parts[:-1]:
            if part not in d or not isinstance(d[part], dict):
                d[part] = {}
            d = d[part]
        d[parts[-1]] = value

    for key, value in flat.items():
        if '.' in key:
            parts = key.split('.')
            set_nested(nested, parts, value)
        else:
            nested[key] = value

    print(f"Loaded {lang} translations (nested): {nested}")  # Дебаг: видишь в консоли
    return nested