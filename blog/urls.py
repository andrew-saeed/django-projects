from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='get_posts'),
    path('tag/<slug:tag_slug>/', views.home, name='get_posts_by_tag'),
    path('<int:post_id>/share/', views.share_post, name='share_post'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.get_post, name='get_post'),
    path('<int:post_id>/comment/', views.comment_on_post, name='comment_on_post'),
    path('search/', views.search, name='search'),
    path('post_like/', views.post_like, name='post_like'),
    path('comment_like/', views.comment_like, name='comment_like'),
    path('bookmark_post/', views.bookmark_post, name='bookmark_post'),
]
