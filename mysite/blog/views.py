from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


# список опубликованных постов с пагинацией по 3 поста (по методичке лаб 2, стр. 9-15)
def post_list(request):
    post_list = Post.published.all()
    # постраничная разбивка: 3 поста на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # если номер страницы не число - отдаем первую
        posts = paginator.page(1)
    except EmptyPage:
        # если номер страницы больше максимума - отдаем последнюю
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


# альтернативное представление на основе классов (CBV) (лаб 2, стр. 16-17)
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# детальный просмотр одного поста по каноническому URL (год/месяц/день/слаг) (лаб 2, стр. 7-8, 44)
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    # список активных комментариев к этому посту
    comments = post.comments.filter(active=True)
    # форма для добавления нового комментария
    form = CommentForm()

    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form
        }
    )


# отправка рекомендации поста по email (лаб 2, стр. 22-28)
def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        # форма была отправлена пользователем
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # поля прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])
            sent = True
    else:
        # пустая форма при GET-запросе
        form = EmailPostForm()

    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )


# обработка отправки формы комментария (лаб 2, стр. 39)
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # создаем объект комментария, но пока не сохраняем в базу (commit=False)
        comment = form.save(commit=False)
        # привязываем комментарий к текущему посту
        comment.post = post
        # теперь сохраняем в базу данных
        comment.save()

    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )
