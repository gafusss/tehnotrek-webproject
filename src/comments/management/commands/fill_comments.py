# coding=utf-8
from django.core.management import BaseCommand
from comments.models import Comment
from exploit.models import Post
from django.contrib.auth import get_user_model
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        posts = list(Post.objects.all())
        users = list(get_user_model().objects.all())
        for i in range(1000):
            c = Comment()
            c.text = u"Комментарий {}".format(i)
            parent_post = random.choice(posts)
            c.parent_post = parent_post
            parent_comments = list(parent_post.comments.all())
            if parent_comments:
                c.parent_comment = random.choice(parent_comments)
            c.author = random.choice(users)
            c.save()

# text parent_post parent_comment author
