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
def student_register(_request, req_js):
    """
    学生端注册
    :param _request:
    :param req_js:
    :return:
    """
    try:
        if len(Student.objects.filter(pho_num=req_js['phoNum'])):
            rep = settings.REP_STATUS[201]
        else:
            student = Student(
                user_name=req_js['userName'],
                stu_id=req_js['stuId'],
                school=req_js['school'],
                college=req_js['college'],
                stu_class=req_js['class'],
                mailbox=req_js['mailbox'],
                pho_num=req_js['phoNum'],
                pass_word=req_js['passWord'])
            student.save()
            rep = settings.REP_STATUS[100]
            rep['data'] = dict(token=student.token)
    except KeyError:
        rep = settings.REP_STATUS[300]
    return JsonResponse(rep, safe=False)


@csrf_exempt
def student_login(request):
    """
    用户端登录
    :param request:
    :return:
    """
    return login(request, lg_type=1)


@auth_permission_required()
def find_clubs(request, user):
    if request.method == 'GET':
        clubs = Club.objects.filter(school=user.school)
        if len(clubs) == 0:
            rep = settings.REP_STATUS[301]
        else:
            rep = settings.REP_STATUS[100]
            rep['data'] = list()
            for club in clubs:
                club_data = dict()
                club_data['clubId'] = club.pk
                club_data['clubName'] = club.club_name
                club_data['clubDesc'] = club.club_desc
                rep['data'].append(club_data)
        return JsonResponse(rep, safe=False)
    else:
        rep = settings.REP_STATUS[111]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required()
@post_log
def club_apply(_request, req_js, stu):
    try:
        club = Club.objects.get(pk=req_js['clubId'])
        rec = Recruitment(
            stu_name=req_js['stuName'],
            stu_id=req_js['stuId'],
            pho_num=req_js['phoNum'],
            mailbox=req_js['mailbox'],
            stu_desc=req_js['stuDesc'],
            Club=club,
            Student=stu
        )
        rec.save()
        rep = settings.REP_STATUS[100]
    except KeyError:
        rep = settings.REP_STATUS[300]
    except Club.DoesNotExist:
        rep = settings.REP_STATUS[211]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required()
@post_log
def find_notices(_request, req_js, _stu):
    try:
        club = Club.objects.get(pk=req_js['clubId'])
        notices = Notice.objects.filter(Club=club).order_by('-date')
        rep = settings.REP_STATUS[100]
        rep['data'] = list()
        for notice in notices:
            notice_dict = dict()
            notice_dict['title'] = notice.title
            notice_dict['text'] = notice.text
            notice_dict['date'] = str(notice.date).split('+')[0]
            rep['data'].append(notice_dict)
    except KeyError:
        rep = settings.REP_STATUS[300]
    except Club.DoesNotExist:
        rep = settings.REP_STATUS[211]
    return JsonResponse(rep, safe=False)

