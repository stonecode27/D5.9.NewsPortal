from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post
from .filters import PostFilter


class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10

class PostAsIs(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 1  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

