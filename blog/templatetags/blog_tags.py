import markdown
from django.conf import settings
from django.templatetags.static import static
from django.db.models import Count
from django.utils.safestring import mark_safe
from django import template
from ..models import Post, LikedItem, Comment, Bookmark
from django.contrib.contenttypes.models import ContentType

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
def has_liked_post(user, post_id):
    if user is None or not user.is_authenticated:
        return 'notauthed'

    post_content_type = ContentType.objects.get_for_model(Post)
    result = LikedItem.objects.filter(
        user=user,
        content_type=post_content_type,
        object_id=post_id
    ).exists()
    return 'liked' if result else 'empty'

@register.simple_tag
def has_liked_comment(user, comment_id):
    if user is None or not user.is_authenticated:
        return 'notauthed'

    comment_content_type = ContentType.objects.get_for_model(Comment)
    result = LikedItem.objects.filter(
        user=user,
        content_type=comment_content_type,
        object_id=comment_id
    ).exists()
    return 'liked' if result else 'empty'

@register.simple_tag
def has_bookmarked_post(user, post_id):
    if user is None or not user.is_authenticated:
        return 'empty'

    result = Bookmark.objects.filter(
        user=user,
        post=post_id,
    ).exists()
    return 'bookmarked' if result else 'empty'