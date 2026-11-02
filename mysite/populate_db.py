import os
import sys
import django
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Comment

user, created = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@admin.com'}
)
if created:
    user.set_password('admin')
    user.is_superuser = True
    user.is_staff = True
    user.save()

posts_data = [
    {
        'title': 'Who was Django Reinhardt?',
        'slug': 'who-was-django-reinhardt',
        'body': 'Jean Reinhardt, known to all by his Romani nickname Django, was a Belgian-born Romani-French jazz guitarist and composer. He was the first major jazz talent to emerge from Europe and remains the most significant.',
        'publish': datetime(2026, 10, 26, 11, 30, tzinfo=timezone.utc),
        'tags': ['django', 'jazz', 'music']
    },
    {
        'title': 'Another post',
        'slug': 'another-post',
        'body': 'Post body with interesting thoughts about web development and Python.',
        'publish': datetime(2026, 10, 26, 15, 45, tzinfo=timezone.utc),
        'tags': ['django', 'python']
    },
    {
        'title': 'Django 4 Features',
        'slug': 'django-4-features',
        'body': 'Django 4 brings many exciting features including async views, zoneinfo timezone support, and more.',
        'publish': datetime(2026, 10, 27, 10, 20, tzinfo=timezone.utc),
        'tags': ['django', 'python']
    },
    {
        'title': 'Understanding Django ORM',
        'slug': 'understanding-django-orm',
        'body': 'The Object-Relational Mapping (ORM) layer in Django allows developers to interact with the database using Python code instead of raw SQL queries.',
        'publish': datetime(2026, 10, 27, 14, 15, tzinfo=timezone.utc),
        'tags': ['django', 'python']
    },
    {
        'title': 'Class-based views vs Function-based views',
        'slug': 'cbv-vs-fbv',
        'body': 'Class-based views provide an alternative way to implement views as Python objects instead of functions.',
        'publish': datetime(2026, 10, 28, 9, 30, tzinfo=timezone.utc),
        'tags': ['django', 'python']
    },
    {
        'title': 'Post formatted with markdown',
        'slug': 'post-formatted-with-markdown',
        'body': '''This is a post formatted with markdown
--------------------------------------
*This is emphasized* and **this is more emphasized**.

Here is a list:
* One
* Two
* Three

And a [link to the Django website](https://www.djangoproject.com/).''',
        'publish': datetime(2026, 10, 28, 14, 0, tzinfo=timezone.utc),
        'tags': ['django', 'markdown', 'music']
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
    if not created_p:
        post_obj.title = p['title']
        post_obj.body = p['body']
        post_obj.publish = p['publish']
        post_obj.status = Post.Status.PUBLISHED
        post_obj.save()
    Post.objects.filter(id=post_obj.id).update(
        created=p['publish'],
        updated=p['publish']
    )
    post_obj.tags.set(p['tags'])

first_post = Post.objects.filter(slug='who-was-django-reinhardt').first()
if first_post:
    c1, _ = Comment.objects.get_or_create(
        post=first_post,
        name='Dias',
        email='dias@example.com',
        body='Great post, very useful!',
        defaults={'active': True}
    )
    Comment.objects.filter(id=c1.id).update(
        created=datetime(2026, 10, 28, 14, 30, tzinfo=timezone.utc),
        updated=datetime(2026, 10, 28, 14, 30, tzinfo=timezone.utc)
    )

print(f'Database populated: {Post.objects.count()} posts, {Comment.objects.count()} comments.')
