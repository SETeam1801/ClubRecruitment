#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)
from django.urls import path
from .views import views

urlpatterns = [
    path('managerSide/register/', views.manager_register, name='manager_register'),
    path('managerSide/login/', views.manager_login, name='manager_login'),
    path('managerSide/clubDesc/', views.club_info, name='club_desc'),
    path('managerSide/findApps/', views.find_apps, name='find_apps'),
    path('managerSide/editNotice/', views.edit_notice, name='edit_notice'),
    path('managerSide/findDept/', views.find_depts, name='find_depts'),
    path('managerSide/addDept/', views.add_dept, name='add_dept'),
    path('managerSide/deleteDept/', views.delete_dept, name='delete_dept'),
    path('managerSide/editRecruitment/', views.edit_recruitment, name='edit_recruitment'),


    path('studentSide/register/', views.student_register, name='student_register'),
    path('studentSide/login/', views.student_login, name='student_login'),
    path('studentSide/findClubs/', views.find_clubs, name='find_clubs'),
    path('studentSide/showClub/<int:club_id>/', views.show_club, name='show_club'),
    path('studentSide/applyClub/', views.club_apply, name='club_apply'),
    path('studentSide/findNotices/<int:page>/', views.find_notices, name='find_notices')
]