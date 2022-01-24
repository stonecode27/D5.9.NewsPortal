from django.urls import path
from .views import PostsList, PostAsIs, Search, NewPost, EditPost, DeletePost

urlpatterns = [
    path('', PostsList.as_view(), name='news'),
    path('<int:pk>', PostAsIs.as_view(), name='post'),
    path('search/', Search.as_view(), name='news_search'),
    path('add/', NewPost.as_view(), name='news_add'),
    path('<int:pk>/edit', EditPost.as_view(), name='news_edit'),
    path('<int:pk>/delete', DeletePost.as_view(), name='news_delete')
]