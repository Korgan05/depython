from django.urls import path
from . import views

# пространство имен приложения для ссылок вида blog:post_detail (лаб 1, стр. 34)
app_name = 'blog'

urlpatterns = [
    # маршруты блога (лаб 2, стр. 6, 29, 41)
    path('', views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list'), # альтернатива на CBV (классах)
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail'
    ),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]
