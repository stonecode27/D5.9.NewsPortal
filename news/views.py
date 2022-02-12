from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm, CategoryForm
from .tasks import hello


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

#     def post(self, request, *args, **kwargs):
#         if request.POST['mtm_with_category']:
#             category_subs = Category.objects.get(id=request.POST['mtm_with_category']).subscribers.all()
#             for sub in category_subs:
#                 send_mail(
#                     subject=f"""News portal: "{request.POST['header']}" """,
#                     message=f'Здравствуй, {sub.username}, Новая статья в твоём любимом разделе!',
#                     html_message=f"""
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Document</title>
# </head>
# <body>
#     <h2>{request.POST['header']}</h2>
#     <p> {request.POST['text'][:70]} </p>
#     <a href="http://127.0.0.1:8000/news/">Полная статья доступна по ссылке
#     </a>
# </body>
# </html>
# """,
#                     from_email='anewspaper@yandex.ru',
#                     recipient_list=[f"{sub.email}"]
#                 )
#         return super().post(request, *args, **kwargs)


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


