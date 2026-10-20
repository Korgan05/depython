"""
Скрипт для быстрого заполнения базы данных тестовыми данными из методички.
Создает суперюзера admin, тестовые посты (для демонстрации пагинации) и комментарии.
Запуск: python populate_db.py
"""
import os
import sys
import django
from datetime import timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Comment
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

now = timezone.now()

# 2. Создаем посты (минимум 4-5 штук, чтобы наглядно показать пагинацию по 3 поста на страницу)
posts_data = [
    {
        'title': 'Who was Django Reinhardt?',
        'slug': 'who-was-django-reinhardt',
        'body': 'Jean Reinhardt, known to all by his Romani nickname Django, was a Belgian-born Romani-French jazz guitarist and composer. He was the first major jazz talent to emerge from Europe and remains the most significant.',
        'publish': now - timedelta(days=4),
    },
    {
        'title': 'Another post',
        'slug': 'another-post',
        'body': 'Post body with interesting thoughts about web development and Python.',
        'publish': now - timedelta(days=3),
    },
    {
        'title': 'Django 4 Features',
        'slug': 'django-4-features',
        'body': 'Django 4 brings many exciting features including async views, zoneinfo timezone support, and more.',
        'publish': now - timedelta(days=2),
    },
    {
        'title': 'Understanding Django ORM',
        'slug': 'understanding-django-orm',
        'body': 'The Object-Relational Mapping (ORM) layer in Django allows developers to interact with the database using Python code instead of raw SQL queries.',
        'publish': now - timedelta(days=1),
    },
    {
        'title': 'Class-based views vs Function-based views',
        'slug': 'cbv-vs-fbv',
        'body': 'Class-based views provide an alternative way to implement views as Python objects instead of functions.',
        'publish': now,
    },
]

for p in posts_data:
    post_obj, created_p = Post.objects.get_or_create(
        slug=p['slug'],
        defaults={
            'title': p['title'],
            'author': user,
            'body': p['body'],
            'status': Post.Status.PUBLISHED,
            'publish': p['publish']
        }
    )

# 3. Добавляем тестовый комментарий к первому посту
first_post = Post.objects.filter(slug='who-was-django-reinhardt').first()
if first_post:
    Comment.objects.get_or_create(
        post=first_post,
        name='Иван Студент',
        email='student@example.com',
        body='Отличный пост! Очень помог разобраться в теме лабы.',
        defaults={'active': True}
    )

print(f'База данных готова! Всего постов: {Post.objects.count()}, комментариев: {Comment.objects.count()}')
