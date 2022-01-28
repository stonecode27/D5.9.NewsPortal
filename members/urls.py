from django.urls import path
from .views import UserRegisterView, become_an_author


urlpatterns = [
    path('become_an_author', become_an_author, name='become_an_author')
]