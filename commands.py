# Команды выполнены в Django Shell

from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment, rate_summator, comments_from_post

# 1. Создать двух пользователей (с помощью метода User.objects.create_user('username')).
User.objects.create_user('Лев Николаевич Толстой')  # Added
User.objects.create_user('Нассим Николас Талеб')  # Added

# 2. Создать два объекта модели Author, связанные с пользователями.
Author.objects.create(one_to_one_relation=User.objects.get(username='Лев Николаевич Толстой'))  # Added
Author.objects.create(one_to_one_relation=User.objects.get(username='Нассим Николас Талеб'))  # Added

# 3. Добавить 4 категории в модель Category.
Category.objects.create(category_name='Cпорт')  # Added
Category.objects.create(category_name='Игры')  # Added
Category.objects.create(category_name='Туризм')  # Added
Category.objects.create(category_name='Здоровье')  # Added

# 4. Добавить 2 статьи и 1 новость.
article_1_text = '''В половине прошлого столетия по дворам села Хабаровки бегала в затрапезном платье босоногая, но веселая, толстая и краснощекая девка Наташка. По заслугам и просьбе отца ее, кларнетиста Саввы, дед мой взял ее в верх - находиться в числе женской прислуги бабушки. Горничная Наташка отличалась в этой должности кротостью нрава и усердием. Когда родилась матушка и понадобилась няня, эту обязанность возложили на Наташку '''
article_2_text = '''С тех пор Наташка сделалась Натальей Савишной и надела чепец: весь запас любви, который в ней хранился, она перенесла на барышню свою. Когда подле матушки заменила ее гувернантка, она получила ключи от кладовой, и ей на руки сданы были белье и вся провизия. Новые обязанности эти она исполняла с тем же усердием и любовью. Она вся жила в барском добре, во всем видела трату, порчу, расхищение и всеми средствами старалась противодействовать'''
news_text = '''Самолёт летит на Вест, расширяя круг тех мест — от страны к другой стране, — где тебя не встретить мне.Обгоняя дни, года, тенью крыльев «никогда» на земле и на воде'''
Post.objects.create(post_author_relation=Author.objects.get(pk=1), news_or_article=Post.article, header='Л.Н. Толстой, неизвестный отрывок1', text=article_1_text)  # Added
Post.objects.create(post_author_relation=Author.objects.get(pk=1), news_or_article=Post.article, header='Л.Н. Толстой, неизвестный отрывок2', text=article_2_text)  # Added
Post.objects.create(post_author_relation=Author.objects.get(pk=2), news_or_article=Post.news, header='Новость от Бродского', text=news_text)  # Added

# 5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
PostCategory.objects.create(post=Post.objects.get(pk=1), category=Category.objects.get(category_name='Cпорт'))  # Added
PostCategory.objects.create(post=Post.objects.get(pk=1), category=Category.objects.get(category_name='Игры'))  # Added
PostCategory.objects.create(post=Post.objects.get(pk=2), category=Category.objects.get(category_name='Туризм'))  # Added
PostCategory.objects.create(post=Post.objects.get(pk=3), category=Category.objects.get(category_name='Здоровье'))  # Added

# 6. Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
Comment.objects.create(otm_post=Post.objects.get(pk=1), otm_user=User.objects.get(pk=2), text='Невероятно!')  # Added
Comment.objects.create(otm_post=Post.objects.get(pk=2), otm_user=User.objects.get(pk=2), text='Восхищению нет предела!')  # Added
Comment.objects.create(otm_post=Post.objects.get(pk=3), otm_user=User.objects.get(pk=1), text='Добавь в друзья')  # Added
Comment.objects.create(otm_post=Post.objects.get(pk=3), otm_user=User.objects.get(pk=1), text='Жду с нетерпением новой статьи')  # Added

# 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
Post.objects.get(pk=1).like()  # Added
Post.objects.get(pk=2).dislike()  # Added
Post.objects.get(pk=3).like()   # Added
Comment.objects.get(pk=1).like()  # Added
Comment.objects.get(pk=2).like()  # Added
Comment.objects.get(pk=3).dislike()  # Added
Comment.objects.get(pk=4).like()  # Added

# 8. Обновить рейтинги пользователей.
Author.objects.get(pk=1).update_rating(rate_summator(1))  # Done
Author.objects.get(pk=2).update_rating(rate_summator(2))  # Done

# 9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
print(f"Лучший автор: {Author.objects.all().order_by('-rate')[0].one_to_one_relation.username}")  # Done
print(f"Его рейтинг: {Author.objects.all().order_by('-rate')[0].rate}")  # Done

# 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
print(f"Лучшая статья: {Post.objects.all().order_by('-rate')[0].header}")  # Done
print(f"Автор статьи: {Post.objects.all().order_by('-rate')[0].post_author_relation.one_to_one_relation.username}")  # Done
print(f"Рейтинг статьи: {Post.objects.all().order_by('-rate')[0].rate}")  # Done
print(f"Дата добавления: {Post.objects.all().order_by('-rate')[0].creation_date}")  # Done
print(f"Предпросмотр: {Post.objects.all().order_by('-rate')[0].preview()}")  # Done

# 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
comments_from_post()  # Done
