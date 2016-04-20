# coding=utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.

class Like(models.Model):
    def __unicode__(self):
        return "{} {}".format(self.user.username, self.item_id)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'Пользователь', related_name='likes')
    value = models.BooleanField(verbose_name=u'Лайк')
    item_type = models.ForeignKey(ContentType)
    item_id = models.PositiveIntegerField()
    item = GenericForeignKey('item_type', 'item_id')

    class Meta:
        verbose_name = u'Лайк'
        verbose_name_plural = u'Лайки'
        unique_together = ('user', 'item_type', 'item_id')
