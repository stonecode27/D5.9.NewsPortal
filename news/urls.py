from django.urls import path
from .views import PostsList, PostAsIs

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostAsIs.as_view())
]