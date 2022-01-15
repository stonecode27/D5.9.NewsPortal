from django.urls import path
from .views import PostsList, PostAsIs, Search

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostAsIs.as_view()),
    path('search/', Search.as_view())
]