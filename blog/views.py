from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import EmailPostForm, CommentForm
from django.views.generic import ListView
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
# from django.http import Http404

def get_posts(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts_list = paginator.page(page_number)
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    return render(request, 'blog/post/list.html', {'posts': posts_list})

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
        comment.save()
    return render(request, 'blog/post/comment.html', {'post':post, 'comment':comment})

def get_post(request, year, month, day, post):
    # try:
    #     post = Post.objects.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('post not found')
    post = get_object_or_404(
        Post, 
        status=Post.Status.PUBLISHED, 
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'blog/post/single.html', {'post': post, 'comments':comments, 'form': form})
