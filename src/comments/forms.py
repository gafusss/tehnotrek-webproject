# coding=utf-8
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'parent_post', 'parent_comment')

    def clean(self):
        data = super(CommentForm, self).clean()
        if not data.get('parent_comment'):
            return data
        if not data.get('parent_comment') in data.get('parent_post').comments.all():
            raise forms.ValidationError(u'Неверное значение родительского комментария')
        return data
