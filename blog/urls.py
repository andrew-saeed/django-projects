from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.get_posts, name='get_posts'),
    path('<int:id>/', views.get_post, name='get_post'),
]
