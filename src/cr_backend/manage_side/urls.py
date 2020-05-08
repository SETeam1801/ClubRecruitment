#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login')
]