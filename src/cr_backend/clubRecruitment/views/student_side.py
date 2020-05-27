#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from ..models import Student, Club, Recruitment, Notice, Department
from .general import auth_permission_required, post_log, login, date_fomat


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


@csrf_exempt
@auth_permission_required()
@post_log
def find_clubs(_request, req_js, user):
    try:
        clubs = Club.objects.filter(school=user.school, club_name__contains=req_js['find'])
        pages = int(len(clubs) / settings.PAGES)
        rep = settings.REP_STATUS[100]
        if req_js['leaft'] <= pages:
            rep['lastPage'] = 0 if req_js['leaft'] < pages else 1
            rep['data'] = list()
            s = pages * settings.PAGES
            e = (req_js['leaft']+1)*settings.PAGES if req_js['leaft']+1 <= pages else len(clubs)
            for club in clubs[s:e]:
                club_data = dict()
                club_data['clubId'] = club.pk
                club_data['clubName'] = club.club_name
                club_data['clubDesc'] = club.club_desc
                club_data['clubPictureUrl'] = settings.DEFAULT_IMG
                rep['data'].append(club_data)
        else:
            rep = settings.REP_STATUS[211]
    except KeyError:
        rep = settings.REP_STATUS[300]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required()
@post_log
def club_apply(_request, req_js, stu):
    try:
        club = Club.objects.get(pk=req_js['clubId'])
        dept = Department.objects.get(pk=req_js['deptId'])
        rec = Recruitment(
            stu_name=req_js['stuName'],
            stu_id=req_js['stuId'],
            pho_num=req_js['phoNum'],
            mailbox=req_js['mailbox'],
            stu_desc=req_js['stuDesc'],
            Club=club,
            Department=dept,
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
def find_notices(_request, stu, page):
    try:
        notices = Notice.objects.filter(Student=stu).order_by('-date')
        pages = int(len(notices) / settings.PAGES)
        rep = settings.REP_STATUS[100]

        if page <= pages:
            rep['lastPage'] = 0 if page < pages else 1
            rep['data'] = list()
            s = pages * settings.PAGES
            e = (page+1)*settings.PAGES if page+1 <= pages else len(notices)
            for notice in notices[s:e]:
                club = notice.Club
                dept = notice.Department
                notice_dict = dict()
                notice_dict['title'] = notice.title
                notice_dict['text'] = notice.text
                notice_dict['date'] = date_fomat(notice.date)
                notice_dict['clubName'] = club.club_name
                notice_dict['deptDesc'] = dept.dept_name
                rep['data'].append(notice_dict)
        else:
            rep = settings.REP_STATUS[211]
    except KeyError:
        rep = settings.REP_STATUS[300]
    except Club.DoesNotExist:
        rep = settings.REP_STATUS[211]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required()
def show_club(_request, _stu, club_id):
    """
    展示社团、部门信息
    :param _request:
    :param _stu:
    :param club_id:
    :return:
    """
    try:
        club = Club.objects.get(pk=int(club_id))
        depts = Department.objects.filter(Club=club)
        rep = settings.REP_STATUS[100]
        rep['data'] = dict()
        rep['data']['clubName'] = club.club_name
        rep['data']['clubDesc'] = club.club_desc
        rep['data']['clubPictureUrl'] = list()
        for i in range(5):
            rep['data']['clubPictureUrl'].append(settings.DEFAULT_IMG)
        rep['data']['dept'] = list()
        for dept in depts:
            dept_dic = dict()
            dept_dic['deptId'] = dept.pk
            dept_dic['deptName'] = dept.dept_name
            dept_dic['status'] = dept.status
            dept_dic['recruitment'] = dict()
            dept_dic['recruitment']["startTime"] = date_fomat(dept.start_time)
            dept_dic['recruitment']["endTime"] = date_fomat(dept.end_time)
            dept_dic['recruitment']["deptId"] = dept.pk
            dept_dic['recruitment']["qq"] = dept.qq
            dept_dic['recruitment']["times"] = dept.times
            dept_dic['recruitment']["maxNum"] = dept.max_num
            dept_dic['recruitment']["standard"] = dept.standard
            dept_dic['recruitment']["add"] = dept.add
            rep['data']['dept'].append(dept_dic)
    except KeyError:
        rep = settings.REP_STATUS[300]
    except Club.DoesNotExist:
        rep = settings.REP_STATUS[211]
    return JsonResponse(rep, safe=False)