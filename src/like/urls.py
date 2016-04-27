from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [
    url(r'^(?P<content_type_id>\d+)/(?P<pk>\d+)/like/$', login_required(views.LikeView.as_view()), {'value': True},
        name='like'),
    url(r'^(?P<content_type_id>\d+)/(?P<pk>\d+)/dislike/$', login_required(views.LikeView.as_view()), {'value': False},
        name='dislike'),
]
