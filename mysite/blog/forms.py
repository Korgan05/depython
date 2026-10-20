from django import forms
from .models import Comment


# форма отправки поста по электронной почте (лаб 2, стр. 20)
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)                    # имя отправителя
    email = forms.EmailField()                               # email отправителя
    to = forms.EmailField()                                  # email получателя
    comments = forms.CharField(                              # необязательный комментарий
        required=False,
        widget=forms.Textarea
    )


# форма для добавления комментариев на основе модели Comment (лаб 2, стр. 38)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # задаем в явном виде, какие поля показывать в форме пользователю
        fields = ['name', 'email', 'body']
