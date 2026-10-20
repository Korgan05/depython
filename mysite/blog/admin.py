from django.contrib import admin
from .models import Post, Comment


# кастомизация админки для постов блога (по методичке лаб 1, стр. 24-26)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']  # колонки в таблице
    list_filter = ['status', 'created', 'publish', 'author']        # боковая панель с фильтрами
    search_fields = ['title', 'body']                               # поиск по заголовку и содержимому
    prepopulated_fields = {'slug': ('title',)}                      # слаг генерируется автоматом при вводе title
    raw_id_fields = ['author']                                      # виджет поиска автора вместо дропдауна
    date_hierarchy = 'publish'                                      # полоса навигации по годам/месяцам
    ordering = ['status', 'publish']                                # порядок сортировки


# регистрация модели комментариев в админке (лаб 2, стр. 36)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']  # видно статус модерации active
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
