from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# кастомный менеджер, чтобы забирать только опубликованные посты (по методичке стр. 30)
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# основная модель поста (лекция 2, слайды 21-28 / методичка стр. 9-17)
class Post(models.Model):
    # статусы поста: черновик или опубликован
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    # связь многие-к-одному с моделью User (при удалении автора удаляются и посты - CASCADE)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )

    # менеджеры
    objects = models.Manager()          # дефолтный
    published = PublishedManager()      # кастомный (Post.published.all())

    class Meta:
        # сортировка по убыванию даты публикации (от новых к старым)
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
