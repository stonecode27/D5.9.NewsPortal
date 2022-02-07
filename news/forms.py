from django.forms import DateInput, ModelForm, CheckboxSelectMultiple, Textarea
from .models import Post, Category


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


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('category_name', 'subscribers')
        labels = {'category_name': 'Категория'}

