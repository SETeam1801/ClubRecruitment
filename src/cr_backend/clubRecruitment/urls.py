#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)
from django.urls import path
from . import views

urlpatterns = [
    path('managerSide/register/', views.manager_register, name='manager_register'),
    path('managerSide/login/', views.manager_login, name='manager_login'),

    path('studentSide/register/', views.student_register, name='student_register'),
    path('studentSide/login/', views.student_login, name='student_login')
]