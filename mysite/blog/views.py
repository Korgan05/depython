from django.shortcuts import render, get_object_or_404
from .models import Post


# список всех опубликованных постов (по методичке стр. 31-32)
def post_list(request):
    posts = Post.published.all()  # берем через наш кастомный менеджер только опубликованные
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


# детальный просмотр одного поста по id (по методичке стр. 32-33)
def post_detail(request, id):
    # get_object_or_404 сразу возвращает 404 ошибку, если пост не найден
    post = get_object_or_404(
        Post,
        id=id,
        status=Post.Status.PUBLISHED
    )
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )
