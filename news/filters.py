from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post
from .forms import DateInputWidget


class PostFilter(FilterSet):
    title_icon = CharFilter(field_name='header', lookup_expr='icontains', label='Заголовок')
    user_name_icon = CharFilter(field_name='post_author_relation__one_to_one_relation__username', lookup_expr='icontains', label='Автор')
    datetime_created__gte = DateFilter(field_name='creation_date', lookup_expr='gte', label='Позднее чем', widget=DateInputWidget)

    class Meta:

        model = Post

        fields = {
        }