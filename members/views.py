from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import RegistrationForm
from django.urls import reverse_lazy
from django.forms import EmailField, CharField
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class UserRegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    email = EmailField(label="Email")
    first_name = CharField(label="Имя")
    last_name = CharField(label="Фамилия")
    success_url = reverse_lazy('login')

@login_required
def become_an_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')