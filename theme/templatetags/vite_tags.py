import json
from django.conf import settings
from django.templatetags.static import static
from django import template

register = template.Library()

@register.simple_tag
def vite_asset(asset_path):
    manifest_file = settings.BASE_DIR / 'static' / 'manifest.json'
    try:
        with open(manifest_file) as f:
            manifest = json.load(f)
        file_path = manifest[asset_path]['file']
        return static(f"{file_path}")
    except Exception as e:
        # Log the error or raise an exception as needed.
        return f"<!-- Error loading asset: {e} -->"