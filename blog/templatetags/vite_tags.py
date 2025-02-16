import json
from django.conf import settings
from django.templatetags.static import static
from django import template
from pathlib import Path

register = template.Library()

@register.simple_tag
def vite_asset(asset_path):
    """
    Returns the URL for the built asset from the Vite manifest.
    Assumes each app's Vite build outputs a manifest.json to:
        BASE_DIR/blog/static/manifest.json
    """
    manifest_file = settings.BASE_DIR / 'blog' / 'static' / 'manifest.json'
    try:
        with open(manifest_file) as f:
            manifest = json.load(f)
        file_path = manifest[asset_path]['file']
        return static(f"{file_path}")
    except Exception as e:
        # Log the error or raise an exception as needed.
        return f"<!-- Error loading asset: {e} -->"