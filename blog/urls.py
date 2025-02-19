from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.get_posts, name='get_posts'),
    path('<int:post_id>/share/', views.share_post, name='share_post'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.get_post, name='get_post'),
    path('<int:post_id>/comment/', views.comment_on_post, name='comment_on_post'),
]
