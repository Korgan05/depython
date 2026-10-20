import os
import sys
import django
from django.utils import timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post

user, created = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@admin.com'}
)
if created:
    user.set_password('admin123')
    user.is_superuser = True
    user.is_staff = True
    user.save()

Post.objects.get_or_create(
    slug='who-was-django-reinhardt',
    defaults={
        'title': 'Who was Django Reinhardt?',
        'author': user,
        'body': 'Jean Reinhardt, known to all by his Romani nickname Django, was a Belgian-born Romani-French jazz guitarist and composer. He was the first major jazz talent to emerge from Europe and remains the most significant.',
        'status': Post.Status.PUBLISHED,
        'publish': timezone.now()
    }
)

Post.objects.get_or_create(
    slug='another-post',
    defaults={
        'title': 'Another post',
        'author': user,
        'body': 'Post body.',
        'status': Post.Status.PUBLISHED,
        'publish': timezone.now()
    }
)

print(f'Total posts: {Post.objects.count()}, Published: {Post.published.count()}')
