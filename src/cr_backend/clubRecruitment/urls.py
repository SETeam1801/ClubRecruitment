#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)
from django.urls import path
from . import views

urlpatterns = [
    path('managerSide/register/', views.manager_register, name='manager_register'),
    path('managerSide/login/', views.manager_login, name='manager_login'),
    path('managerSide/clubDesc/', views.club_info, name='club_desc'),
    path('managerSide/findApps/', views.find_apps, name='find_apps'),
    path('managerSide/editNotice/', views.edit_notice, name='edit_notice'),

    path('studentSide/register/', views.student_register, name='student_register'),
    path('studentSide/login/', views.student_login, name='student_login'),
    path('studentSide/findClubs/', views.find_clubs, name='find_clubs'),
    path('studentSide/applyClub/', views.club_apply, name='club_apply'),
    path('studentSide/findNotices/', views.find_notices, name='find_notices')
]