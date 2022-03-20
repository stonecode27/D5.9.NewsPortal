from django.db.models.signals import post_save, m2m_changed
from django.core.signals import request_started
from allauth.account.signals import email_confirmed
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver

from allauth.account.models import EmailAddress
from .models import Category, Post
from .tasks import send_post_notify, print_hello


@receiver(m2m_changed)
def new_post_email_notify(sender, instance, **kwargs):
    print(instance)
    if kwargs['action'] == "post_add":
        for category in instance.mtm_with_category.all():  # instance's all categories iteration
            for sub in category.subscribers.all():  # category's all subs iteration
                if sub:
                    subject=f"""NewsPortal: Новая статья в категории {category}"""
                    text_content=f"""
Здравствуй, {sub.username}, На сайте новая статья - {instance.header}.
{instance.text[:50]}...
Полная версия доступна по ссылке: http://127.0.0.1:8000/news/{instance.id}
"""
                    send_post_notify.delay(subject, text_content, sub.email)


@receiver(email_confirmed)
def welcome(request, email_address, **kwargs):
    subject = f"""{email_address.user.username}, email - подтвержден!"""
    text_content = f'Здравствуй, {email_address.user.username}, добро пожаловать на сайт NewsPortal'
    with open('templates/emails/welcome.html') as html_content:
        msg = EmailMultiAlternatives(subject, text_content, "anewsportal@mail.ru", [email_address.email])
        msg.attach_alternative(html_content.read(), "text/html")
        msg.send()

# @receiver(request_started)
# def call_hello(**kwargs):
#     print_hello()