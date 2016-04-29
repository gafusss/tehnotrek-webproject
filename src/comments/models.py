# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from like.models import LikeMixin
from .tasks import send_email_notification


# Create your models here.

class Comment(LikeMixin):
    def __unicode__(self):
        return 'Post: %20s' % self.text

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('exploit:post', args=[str(self.parent_post.id)]) + "#article-comment-" + str(self.id)

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

    def as_compact_dict(self):
        result = {}
        if self.parent_comment:
            result = {'id': self.id,
                      'text': self.text,
                      'parent_post': self.parent_post.pk,
                      'parent_comment': self.parent_comment.pk,
                      'author': self.author.username}
        else:
            result = {'id': self.id,
                      'text': self.text,
                      'parent_post': self.parent_post.pk,
                      'author': self.author.username}
        return result


@receiver(post_save, sender=Comment, dispatch_uid="post_save_comment_centrifugo")
def comment_post_save(sender, instance=None, **kwargs):
    from adjacent import Client
    client = Client()
    client.publish(instance.parent_post.get_cent_answers_channel_name(), instance.as_compact_dict())
    response = client.send()
    print(
        'sent to channel {}, got response from centrifugo: {}'.format(
            instance.parent_post.get_cent_answers_channel_name(),
            response))


@receiver(post_save, sender=Comment, dispatch_uid="post_save_comment_email")
def on_comment_creation(sender, instance, *args, **kwargs):
    if kwargs.get('created'):
        comment = instance
        send_email_notification.delay(
            'A.gafusss.A@gmail.com',
            'New answer to question "{}"'.format(comment.parent_post.title),
            'You got answer with the text: "{}"'.format(comment.text)
        )
