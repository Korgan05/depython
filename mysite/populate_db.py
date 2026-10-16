"""
Скрипт для быстрого заполнения базы данных тестовыми данными из методички.
Создает суперюзера admin и 2 тестовых поста.
Запуск: python populate_db.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post
from django.utils import timezone

# 1. Создаем админа для входа в панель управления (admin / admin123)
user, created = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@admin.com'}
)
if created:
    user.set_password('admin123')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print('Суперпользователь admin создан (логин: admin, пароль: admin123)')
else:
    print('Пользователь admin уже есть в базе')

# 2. Создаем посты из примера на стр. 38 методички
post1, created1 = Post.objects.get_or_create(
    slug='who-was-django-reinhardt',
    defaults={
        'title': 'Who was Django Reinhardt?',
        'author': user,
        'body': 'Jean Reinhardt, known to all by his Romani nickname Django, was a Belgian-born Romani-French jazz guitarist and composer. He was the first major jazz talent to emerge from Europe and remains the most significant.',
        'status': Post.Status.PUBLISHED,
        'publish': timezone.now()
    }
)

post2, created2 = Post.objects.get_or_create(
    slug='another-post',
    defaults={
        'title': 'Another post',
        'author': user,
        'body': 'Post body.',
        'status': Post.Status.PUBLISHED,
        'publish': timezone.now()
    }
)

print(f'База данных готова! Всего постов: {Post.objects.count()}, опубликовано: {Post.published.count()}')
