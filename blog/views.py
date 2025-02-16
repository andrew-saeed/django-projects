from django.shortcuts import render, get_object_or_404
from .models import Post
# from django.http import Http404

def get_posts(request):
    posts = Post.objects.all()
    return render(request, 'blog/post/list.html', {'posts': posts})

def get_post(request, id):
    # try:
    #     post = Post.objects.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('post not found')
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, 'blog/post/single.html', {'post': post})


