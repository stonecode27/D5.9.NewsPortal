from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver

import datetime
from .models import Post


@shared_task
def send_post_notify(subject, text_content, subscriber_email):
    print("Start sending message")
    msg=EmailMultiAlternatives(subject, text_content, "anewsportal@mail.ru", [subscriber_email])
    msg.send()


@shared_task
def weekly_category_digest():
    weekly_posts = Post.objects.filter(creation_date__gte=(datetime.datetime.now() - datetime.timedelta(days=7)))
    for post in weekly_posts:
        for category in post.mtm_with_category.all():  # instance's all categories iteration
            links_list = [f'http://127.0.0.1:8000/news/{key.id}' for key in weekly_posts.filter(mtm_with_category=category)]
            links_string = '\n'.join(links_list)
            for sub in category.subscribers.all():  # category's all subs iteration
                if sub:
                    subject = f"""NewsPortal: Подборка статей за неделю в категории {category}"""
                    text_content = f"""
        Здравствуй, {sub.username}, за прошлую неделю категория - {category} пополнилась следующими статьями:
        {links_string}
        """
                    msg = EmailMultiAlternatives(subject, text_content, "anewsportal@mail.ru", [sub.email])
                    msg.send()