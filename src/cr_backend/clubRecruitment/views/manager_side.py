#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)
from django.http import JsonResponse
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from ..models import Admin, Student, Club, Recruitment, Notice
from .general import auth_permission_required, post_log, login


@csrf_exempt
@post_log
def manager_register(_request, req_js):
    """

    :param _request:
    :param req_js:
    :return:
    """
    try:
        if len(Admin.objects.filter(pho_num=req_js['phoNum'])):
            rep = settings.REP_STATUS[201]
        else:
            admin = Admin(
                user_name=req_js['userName'],
                pass_word=req_js['passWord'],
                stu_id=req_js['stuId'],
                pho_num=req_js['phoNum'])
            club = Club(
                club_name=req_js['clubName'],
                school=req_js['school'],
                club_desc='',
                Admin=admin
            )
            admin.save()
            club.save()
            rep = settings.REP_STATUS[100]
            rep['data'] = dict(token=admin.token)
    except KeyError:
        rep = settings.REP_STATUS[300]
    return JsonResponse(rep, safe=False)


@csrf_exempt
def manager_login(request):
    """
    管理端登录
    :param request:
    :return:
    """
    return login(request, lg_type=0)


@csrf_exempt
@auth_permission_required(user_type='admin')
@post_log
def club_info(_request, req_js, user):
    """

    :param _request:
    :param req_js:
    :param user:
    :return:
    """
    admin = user
    club = Club.objects.get(Admin=admin)
    club.club_desc = req_js['desc']
    club.save()
    rep = settings.REP_STATUS[100]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
def find_apps(request, admin):
    if request.method == 'GET':
        club = Club.objects.get(Admin=admin)
        apps = Recruitment.objects.filter(Club=club)
        if len(apps) == 0:
            rep = settings.REP_STATUS[301]
        else:
            rep = settings.REP_STATUS[100]
            rep['data'] = list()
            for app in apps:
                club_data = dict()
                club_data['stuName'] = app.stu_name
                club_data['stuId'] = app.stu_id
                club_data['stuDesc'] = app.stu_desc
                club_data['mailbox'] = app.mailbox
                club_data['phoNum'] = app.pho_num
                rep['data'].append(club_data)
        return JsonResponse(rep, safe=False)
    else:
        rep = settings.REP_STATUS[111]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
@post_log
def edit_notice(_request, req_js, admin):
    try:
        club = Club.objects.get(Admin=admin)
        notice = Notice(
            text=req_js['text'],
            title=req_js['title'],
            date=req_js['date'],
            Club=club
        )
        notice.save()
        rep = settings.REP_STATUS[100]
    except KeyError:
        rep = settings.REP_STATUS[300]
    return JsonResponse(rep, safe=False)




