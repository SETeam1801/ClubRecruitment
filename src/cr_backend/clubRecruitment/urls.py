#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import views

urlpatterns = [
    path('managerSide/register/', views.manager_register, name='manager_register'),
    path('managerSide/login/', views.manager_login, name='manager_login'),
    path('managerSide/clubDesc/', views.add_club_info, name='club_desc'),
    path('managerSide/findApps/<int:dept_id>/', views.find_apps, name='find_apps'),
    path('managerSide/editNotice/', views.edit_notice, name='edit_notice'),
    path('managerSide/findDept/', views.find_depts, name='find_depts'),
    path('managerSide/addDept/', views.add_dept, name='add_dept'),
    path('managerSide/deleteDept/', views.delete_dept, name='delete_dept'),
    path('managerSide/editRecruitment/', views.edit_recruitment, name='edit_recruitment'),
    path('managerSide/uploadImg/', views.upload_img, name='upload_img'),
    path('managerSide/sendMails/', views.send_mails, name='send_mails'),
    path('managerSide/clubInfo/', views.club_info, name='club_info'),
    path('managerSide/findStu/<int:app_id>/', views.stu_info, name='stu_info'),

    path('studentSide/register/', views.student_register, name='student_register'),
    path('studentSide/login/', views.student_login, name='student_login'),
    path('studentSide/findClubs/', views.find_clubs, name='find_clubs'),
    path('studentSide/showClub/<int:club_id>/', views.show_club, name='show_club'),
    path('studentSide/applyClub/', views.club_apply, name='club_apply'),
    path('studentSide/findNotices/<int:page>/', views.find_notices, name='find_notices'),
    path('studentSide/uploadAvatar/', views.upload_avatar, name='upload_avatar'),
    path('studentSide/enteredPage/', views.entered_page, name='entered_page'),
    path('studentSide/changePersonalInformation/', views.change_info, name='change_info'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
