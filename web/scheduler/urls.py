# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from . import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^scheduler/$', views.scheduler, name='scheduler'),
]