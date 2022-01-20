from django.urls import path
from .views import PostsList, PostAsIs, Search, NewPost, EditPost, DeletePost

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostAsIs.as_view()),
    path('search/', Search.as_view()),
    path('add/', NewPost.as_view()),
    path('<int:pk>/edit', EditPost.as_view()),
    path('<int:pk>/delete', DeletePost.as_view())
]