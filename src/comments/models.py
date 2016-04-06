# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


# Create your models here.

class Comment(models.Model):
    def __unicode__(self):
        return 'Post: %20s' % self.text

    text = models.TextField(verbose_name=u'Комментарий')
    parent_post = models.ForeignKey('exploit.Post', verbose_name=u'Родительский эксплоит', related_name='comments')
    parent_comment = models.ForeignKey('self', models.CASCADE, blank=True, null=True,
                                       verbose_name=u'Родительский комментарий', related_name='replies')
    published = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата публикации')
    modified = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'Автор', related_name='comments')

    # TODO: validators?

    class Meta:
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'
