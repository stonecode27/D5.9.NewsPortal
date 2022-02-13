from django.urls import path
from .views import PostsList, PostAsIs, Search, NewPost, EditPost, DeletePost, CategorySubscribe, Categories
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(PostsList.as_view()), name='news'),
    path('<int:pk>', PostAsIs.as_view(), name='post'),
    path('search/', Search.as_view(), name='news_search'),
    path('add/', NewPost.as_view(), name='news_add'),
    path('<int:pk>/edit', EditPost.as_view(), name='news_edit'),
    path('<int:pk>/delete', DeletePost.as_view(), name='news_delete'),
    path('categories/', cache_page(60*5)(Categories.as_view()), name='categories'),
    path('category/<int:pk>/subscribe', cache_page(60*5)(CategorySubscribe.as_view()), name='category_subscribe')
]