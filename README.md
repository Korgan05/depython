# Лабораторные работы по Python / Django

Проект выполнен строго по лекционным материалам и книге «Django 4 в примерах» (А. Меле).

---

## 1. Быстрое переключение между работами (через ветки Git)

Для защиты перед преподавателем можно мгновенно переключаться между версиями:

* **Показать Лабораторную №1**:
  ```powershell
  git checkout lab1
  ```
* **Показать Лабораторную №2**:
  ```powershell
  git checkout lab2
  ```

---

## 2. Запуск проекта и авторизация

1. Перейдите в папку проекта:
   ```powershell
   cd "c:\Users\Korgan\OneDrive\Рабочий стол\Лаб\7 семестр\Пайтон\mysite"
   ```

2. Запустите сервер разработки:
   ```powershell
   ..\my_env\Scripts\python.exe manage.py runserver
   ```

3. Данные администратора:
   - **URL панели администрирования**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
   - **Логин**: `admin`
   - **Пароль**: `admin123`

*(Если база данных пустая или удалена, команда `..\my_env\Scripts\python.exe populate_db.py` за секунду создаст админа, 5 постов и комментарии).*

---

## 3. Что сделано в Лабораторной работе №1 (ветка `lab1`)

1. **Создание виртуального окружения** `my_env` и установка Django 4.
2. **Инициализация проекта** `mysite` и приложения `blog` (`INSTALLED_APPS` в `settings.py`).
3. **Модель `Post`** (`blog/models.py`):
   - Поля: `title`, `slug`, `author` (связь с `User` через `ForeignKey` с `CASCADE`), `body`, `publish`, `created`, `updated`, `status` (`Draft` / `Published`).
   - Метаданные: `ordering = ['-publish']` и индекс по дате.
   - Кастомный менеджер `PublishedManager` (`Post.published.all()`) для фильтрации черновиков.
4. **Админка `PostAdmin`** (`blog/admin.py`): `list_display`, `list_filter`, `search_fields`, `prepopulated_fields`, `date_hierarchy`.
5. **Представления и шаблоны**: `post_list` и `post_detail` (по `id`), базовый шаблон `base.html`, наследование, фильтры `truncatewords` и `linebreaks`, стили `blog.css`.

---

## 4. Что сделано в Лабораторной работе №2 (ветка `lab2`)

1. **Канонические SEO-friendly URL-адреса**:
   - Метод `get_absolute_url()` в модели `Post` на основе функции `reverse()`.
   - Маршрут вида `/blog/<year>/<month>/<day>/<slug>/` вместо числового id.
   - `unique_for_date='publish'` для поля `slug`.
2. **Постраничная разбивка (Пагинация)**:
   - Вьюха `post_list` использует класс `Paginator` (по 3 поста на страницу) с обработкой `PageNotAnInteger` и `EmptyPage`.
   - Шаблон `pagination.html` с кнопками переключения страниц `Previous` / `Next`.
   - Реализован альтернативный классовый вид `PostListView(ListView)` (CBV).
3. **Формы и отправка Email**:
   - `forms.py`: форма `EmailPostForm(forms.Form)` с полями `name`, `email`, `to`, `comments`.
   - Настройка `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` в `settings.py` (письма логируются прямо в терминал сервера без настройки внешних SMTP).
   - Вьюха `post_share` и шаблон `blog/post/share.html`.
4. **Система комментариев**:
   - Модель `Comment` (`post`, `name`, `email`, `body`, `created`, `updated`, `active`).
   - Модельная форма `CommentForm(forms.ModelForm)` на базе модели `Comment`.
   - Регистрация `CommentAdmin` в `admin.py` с фильтром по `active` (ручная модерация спама).
   - Вьюха `post_comment` с декоратором `@require_POST` и сохранением через `form.save(commit=False)` для связки с постом.
   - Шаблоны: `comment_form.html`, `comment.html` и вывод списка комментариев со счетчиком `comments.count` и фильтром `pluralize` в `detail.html`.

---

## 5. Шпаргалка для защиты (готовые ответы на вопросы преподавателя)

### Вопрос 1: Зачем нужен метод `get_absolute_url()` и функция `reverse()`?
> **Ответ:** Метод `get_absolute_url()` задает единый канонический URL для объекта модели. Функция `reverse()` строит этот URL динамически по имени маршрута (`blog:post_detail`) и переданным параметрам (год, месяц, день, слаг), чтобы не писать ссылки вручную (hardcode) в шаблонах и вьюхах.

### Вопрос 2: Как работает пагинация в Django?
> **Ответ:** Класс `Paginator` принимает queryset и количество элементов на странице (у нас 3). Метод `paginator.page(page_number)` возвращает объект нужной страницы `Page`. Если номер не число — перехватываем `PageNotAnInteger` и отдаем 1-ю страницу. Если номер превышает максимум — перехватываем `EmptyPage` и отдаем последнюю страницу.

### Вопрос 3: В чем разница между `forms.Form` и `forms.ModelForm`?
> **Ответ:** 
> - `forms.Form` (как наша `EmailPostForm`) создается вручную: мы сами описываем все поля (`CharField`, `EmailField`) для данных, которые не сохраняются в базу напрямую.
> - `forms.ModelForm` (как `CommentForm`) строится на основе модели (`model = Comment`). Она автоматически наследует типы полей, валидацию и виджеты из модели, а также умеет сохранять запись в БД вызовом `form.save()`.

### Вопрос 4: Что делает `commit=False` в строчке `comment = form.save(commit=False)`?
> **Ответ:** Создает экземпляр модели в памяти, но не выполняет `INSERT` в базу данных сразу. Это необходимо, чтобы мы могли сначала присвоить внешний ключ `comment.post = post` (привязать комментарий к конкретному посту), а уже затем вызвать `comment.save()`.

### Вопрос 5: Зачем нужен декоратор `@require_POST`?
> **Ответ:** Он запрещает доступ к представлению любыми HTTP-методами, кроме `POST`. Если кто-то попробует перейти по ссылке обычным `GET`-запросом, Django вернет ошибку `405 Method Not Allowed`.

### Вопрос 6: Зачем в модели комментариев поле `active = BooleanField(default=True)`?
> **Ответ:** Для модерации. При выводе на сайте мы фильтруем только `post.comments.filter(active=True)`. Если администратор найдет спам или мат, ему не нужно удалять запись — достаточно снять галочку `active` в панели админки.
