from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    one_to_one_relation = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    def update_rating(self, new_rating):
        self.rate = new_rating
        self.save()

    def __str__(self):
        return self.one_to_one_relation.username


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    article = 'AR'
    news = 'News'

    TYPES = [
        (article, 'ARTICLE'),
        (news, 'NEWS')
    ]

    post_author_relation = models.ForeignKey(Author, on_delete=models.CASCADE)
    news_or_article = models.CharField(max_length=4, choices=TYPES)
    creation_date = models.DateTimeField(auto_now_add=True)
    mtm_with_category = models.ManyToManyField(Category)
    header = models.CharField(max_length=255)
    text = models.TextField()
    rate = models.IntegerField(default=0)

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -=1
        self.save()

    def preview(self):
        limit = 124 if len(self.text) > 124 else len(self.text)
        return self.text[:limit] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    otm_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    otm_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -=1
        self.save()

def rate_summator(id: int):  #  id=pk ????????????
    a = (sum([some_post.rate*3 for some_post in Post.objects.filter(post_author_relation=id)])
        + sum([comment.rate for comment in Comment.objects.filter(otm_user=id)])
        + sum([comment.rate for comment in Comment.objects.filter(otm_post__post_author_relation=id)]))
    return a


def comments_from_post():  # ?????????? ???????? ???????????????????????? ?????????? ???????????? ????????????
    print("?????????????????????? ?? ?????????????? ??????????")
    for comment in Comment.objects.filter(otm_post=Post.objects.all().order_by('-rate')[0]):
        print(f"????????: {comment.creation_time}")
        print(f"????????????????????????: {comment.otm_user.username}")
        print(f"?????????????? ????????????????????: {comment.rate}")
        print(f"""?????????? ??????????????????????: {comment.text}""")