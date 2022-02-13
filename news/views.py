from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache

from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm, CategoryForm


class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostAsIs(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            print('****Object has been recorded to cache')
        return obj


class Search(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-id')
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewPost(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    form_class = PostForm
    permission_required = ('news.add_post', 'news.change_post')


class EditPost(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'edit.html'
    form_class = PostForm
    permission_required = ('news.add_post', 'news.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class DeletePost(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.add_post', 'news.change_post')


class Categories(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.order_by('-id')


class CategorySubscribe(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'category_subscribe.html'
    form_class = CategoryForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Category.objects.get(pk=id)

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        subs = Category.objects.get(pk=id).subscribers.all()
        if request.user in subs:
            return HttpResponse('Вы подписаны')
        else:
            Category.objects.get(pk=id).subscribers.add(request.user)
            return HttpResponseRedirect('/')


