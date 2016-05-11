# coding=utf-8
from django.core.management import BaseCommand
from comments.models import Comment
from exploit.models import Post
from like.models import LikeMixin
from django.contrib.auth import get_user_model
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model in LikeMixin.__subclasses__():
            for object in model.objects.all():
                object.rating = object.get_rating()
                object.save()
