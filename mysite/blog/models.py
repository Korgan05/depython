from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# кастомный менеджер, чтобы забирать только опубликованные посты (по методичке стр. 30)
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# основная модель поста (лекция 2 / лаб 1-2)
class Post(models.Model):
    # статусы поста: черновик или опубликован
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'  # слаг должен быть уникальным для даты публикации (лаб 2, стр. 5)
    )
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
    objects = models.Manager()          # дефолтный менеджер
    published = PublishedManager()      # кастомный менеджер (Post.published.all())

    class Meta:
        # сортировка по убыванию даты публикации (от новых к старым)
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # канонический URL для поста (год/месяц/день/слаг) (лаб 2, стр. 3, 8)
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )


# модель комментариев к посту (лаб 2, стр. 35)
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'  # обратная связь: post.comments.all()
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)  # флаг для модерации комментариев вручную

    class Meta:
        ordering = ['created']  # сортируем по дате добавления (хронологически)
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
