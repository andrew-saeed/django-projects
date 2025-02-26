import json
import markdown
from django.conf import settings
from django.templatetags.static import static
from django.db.models import Count
from django.utils.safestring import mark_safe
from django import template
from ..models import Post

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.simple_tag
def get_most_commented_posts(count):
    return Post.published.annotate(
        total_comments = Count('comments')
    ).order_by('-total_comments')[:count]

@register.inclusion_tag('blog/post/older_posts.html')
def older_posts(count):
    return {'posts': Post.published.order_by('publish')[:count]}

@register.simple_tag
def total_blog_posts():
    return Post.published.count()

@register.simple_tag
def vite_asset(asset_path):
    """
    Returns the URL for the built asset from the Vite manifest.
    Assumes each app's Vite build outputs a manifest.json to:
        BASE_DIR/blog/static/manifest.json
    """
    manifest_file = settings.BASE_DIR / 'static' / 'manifest.json'
    try:
        with open(manifest_file) as f:
            manifest = json.load(f)
        file_path = manifest[asset_path]['file']
        return static(f"{file_path}")
    except Exception as e:
        # Log the error or raise an exception as needed.
        return f"<!-- Error loading asset: {e} -->"