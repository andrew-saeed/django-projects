from django.shortcuts import render, get_object_or_404, redirect
from taggit.models import Tag
from .models import Post, LikedItem, Comment, Bookmark
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

def home(request, tag_slug=None):
    posts = Post.objects.select_related('author').prefetch_related('tags')
    tag = None
    bookmarked_post_ids = set()
    list_paginated = request.GET.get('list-paginated', 0)

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page', 1)

    try:
        posts_list = paginator.page(page_number)
    except EmptyPage:
        if list_paginated:
            return HttpResponse('')
    except PageNotAnInteger:
        posts_list = paginator.page(1)

    discuss_posts = Post.objects.filter(tags__name__in=['discuss'])[0:5]

    tags = Tag.objects.all()

    if request.user.is_authenticated:
        bookmarked_post_ids = set(
            Bookmark.objects.filter(user=request.user).values_list('post_id', flat=True)
        )

    if list_paginated:
        return render(request, 'blog/post/list-paginated.html', {
            'posts': posts_list, 
            'tag': tag, 
            'discuss_posts': discuss_posts, 
            'tags': tags,
            'bookmarked_post_ids': bookmarked_post_ids
        })    
    return render(request, 'blog/home.html', {
        'posts': posts_list, 
        'tag': tag, 
        'discuss_posts': discuss_posts, 
        'tags': tags,
        'bookmarked_post_ids': bookmarked_post_ids
    })

def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid:
            send_mail(
                subject='subject 1',
                message='message 1',
                from_email=None,
                recipient_list = ['recipient_list 1']
            )
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})

@require_POST
def comment_on_post(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect(post.get_absolute_url())

def get_post(request, year, month, day, post):
    post = get_object_or_404(
        Post.objects.select_related('author'), 
        status=Post.Status.PUBLISHED, 
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    comments = post.comments.filter(active=True).select_related('author')
    form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-publish')[:4]

    content_type = ContentType.objects.get_for_model(Post)
    like_count = LikedItem.objects.filter(content_type=content_type, object_id=post.id).count()

    comment_content_type = ContentType.objects.get_for_model(Comment)
    liked_comments = Comment.objects.filter(
        post=post,
        id__in=LikedItem.objects.filter(
            content_type=comment_content_type,
            object_id__in=post.comments.values_list('id', flat=True)
        ).values_list('object_id', flat=True)
    )
    liked_comments_set = set(liked_comments.values_list("id", flat=True))

    bookmarks_count = Bookmark.objects.filter(post=post).count()

    return render(
        request, 
        'blog/single-post.html', 
        {
            'post': post, 
            'comments': comments,
            'comments_count': comments.count(),
            'bookmarks_count': bookmarks_count,
            'like_count': like_count,
            'form': form,
            'similar_posts': similar_posts,
            'liked_comments_set': liked_comments_set
        }
    )

def search(request):
    return render(request, 'blog/search.html')

@login_required
@require_POST
def post_like(request):
    action = request.POST.get('action')
    post_id = request.POST.get('id')
    
    content_type = ContentType.objects.get_for_model(Post)

    if action == 'like':
        LikedItem.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=post_id
        )
    else:
        LikedItem.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=post_id
        ).delete()
    return JsonResponse({'action':action})

@login_required
@require_POST
def comment_like(request):
    action = request.POST.get('action')
    comment_id = request.POST.get('id')
    
    content_type = ContentType.objects.get_for_model(Comment)

    if action == 'like':
        LikedItem.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=comment_id
        )
    else:
        LikedItem.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=comment_id
        ).delete()
    return JsonResponse({'action':action})

@login_required
@require_POST
def bookmark_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    action = request.POST.get('action')

    if action == 'bookmark':
        Bookmark.objects.get_or_create(
            post=post,
            user=request.user
        )
    else:
        Bookmark.objects.filter(
            post=post,
            user=request.user
        ).delete()

    return JsonResponse({'action':action})