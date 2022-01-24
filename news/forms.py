from django.forms import DateInput, ModelForm, CheckboxSelectMultiple, Textarea
from .models import Post, Author


class DateInputWidget(DateInput):
    input_type = 'date'


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('post_author_relation', 'news_or_article', 'mtm_with_category', 'header', 'text')
        labels = {
            'post_author_relation': 'Автор',
            'news_or_article': 'Тип записи',
            'mtm_with_category': 'Категории (одна или несколько)',
            'header': 'Заголовок',
            'text': 'Текст статьи'
        }
        widgets = {
        }
