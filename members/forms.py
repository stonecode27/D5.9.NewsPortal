from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User, Group
from django.forms import CharField, PasswordInput, EmailField
from allauth.account.forms import SignupForm


class RegistrationForm(UserCreationForm):
    password1 = CharField(
        label='Пароль',
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Придумайте пароль, который сможете вспомнить, но не сможет подобрать злоумышленник",
    )
    password2 = CharField(
        label="Подтверждение пароля",
        widget=PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Введите пароль повторно для подтверждения",
    )
    email = EmailField(label="Email")
    first_name = CharField(label="Имя")
    last_name = CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)
        labels = {"username":"Имя пользователя"}
        field_classes = {'username': UsernameField}


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user