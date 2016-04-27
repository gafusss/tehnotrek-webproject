# coding=utf-8
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.

class Like(models.Model):
    def __unicode__(self):
        return "{} {}".format(self.user.username, self.item_id)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'Пользователь', related_name='likes')
    value = models.BooleanField(verbose_name=u'Лайк')
    created_at = models.DateTimeField(auto_now=True)
    item_type = models.ForeignKey(ContentType)
    item_id = models.PositiveIntegerField()
    item = GenericForeignKey('item_type', 'item_id')

    class Meta:
        verbose_name = u'Лайк'
        verbose_name_plural = u'Лайки'
        unique_together = ('user', 'item_type', 'item_id')


class LikeMixin(models.Model):
    likes = GenericRelation(Like, content_type_field='item_type', object_id_field='item_id')

    @models.permalink
    def get_like_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return 'rating:like', (), {'content_type_id': content_type.id, 'pk': self.id}

    @models.permalink
    def get_dislike_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return 'rating:dislike', (), {'content_type_id': content_type.id, 'pk': self.id}

    class Meta:
        abstract = True
