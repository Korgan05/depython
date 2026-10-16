from django.urls import path
from . import views

# пространство имен приложения, чтобы в шаблонах обращаться как blog:post_list (стр. 34)
app_name = 'blog'

urlpatterns = [
    # маршруты приложения blog
    path('', views.post_list, name='post_list'),
    path('<int:id>/', views.post_detail, name='post_detail'),
]
