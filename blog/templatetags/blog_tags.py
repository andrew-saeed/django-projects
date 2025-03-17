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