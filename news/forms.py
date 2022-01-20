from django.forms import DateInput, ModelForm
from .models import Post


class DateInputWidget(DateInput):
    input_type = 'date'


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_author_relation', 'header', 'news_or_article', 'mtm_with_category', 'text']
