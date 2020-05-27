#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)
from django.http import JsonResponse
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from ..models import Admin, Student, Club, Recruitment, Notice
import jwt
import datetime
# TODO
# 1. 信息展示模块
# 2. 学生端登陆注册


def auth_permission_required(user_type='stu'):
    """
    token验证装饰器
    :param perm:
    :param user_type:
    :return:
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # 格式化权限
            user = None
            print(request.META.get('HTTP_AUTHORIZATION'))

            try:
                auth = request.META.get('HTTP_AUTHORIZATION').split()

            except AttributeError:
                return JsonResponse(settings.REP_STATUS[210])

            # 用户通过API获取数据验证流程
            if auth[0].lower() == 'bearer':
                try:
                    token = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
                    print('token验证成功, %s' % token)
                    user_id = token['data']['id']
                except jwt.ExpiredSignatureError:
                    return JsonResponse(settings.REP_STATUS[110])
                except jwt.InvalidTokenError:
                    return JsonResponse(settings.REP_STATUS[101])

                if user_type == 'stu':
                    try:
                        user = Student.objects.get(pk=user_id)
                    except Student.DoesNotExist:
                        return JsonResponse(settings.REP_STATUS[211])
                elif user_type == 'admin':
                    try:
                        user = Admin.objects.get(pk=user_id)
                    except Admin.DoesNotExist:
                        return JsonResponse(settings.REP_STATUS[211])
            else:
                return JsonResponse(settings.REP_STATUS[210])
            return view_func(request, user, *args, **kwargs)
        return _wrapped_view
    return decorator


def post_log(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # 格式化权限
        if request.method == 'POST':
            post_body = request.body
            req_js = json.loads(post_body)
            print('post_body: %s' % req_js)
        else:
            rep = settings.REP_STATUS[111]
            return JsonResponse(rep, safe=False)
        return view_func(request, req_js, *args, **kwargs)
    return _wrapped_view


def login(request, lg_type):
    """
    login的基层函数
    :param request:
    :param lg_type:
    :return:
    """
    if request.method == 'POST':
        post_body = request.body
        req_js = json.loads(post_body)
        print(req_js)
        if lg_type == 0:
            try:
                user = Admin.objects.get(pho_num=req_js['phoNum'])
                club = Club.objects.get(Admin=user)
                if user.pass_word != req_js['passWord']:
                    rep = settings.REP_STATUS[310]
                else:
                    rep = settings.REP_STATUS[100]
                    rep['data'] = dict(
                        userName=user.user_name,
                        school=club.school,
                        clubName=club.club_name,
                        stuId=user.stu_id,
                        token=user.token)
            except KeyError:
                rep = settings.REP_STATUS[300]
            except Admin.DoesNotExist:
                rep = settings.REP_STATUS[211]
            except AttributeError:
                rep = settings.REP_STATUS[200]
        elif lg_type == 1:
            try:
                student = Student.objects.get(pho_num=req_js['phoNum'])
                if student.pass_word != req_js['passWord']:
                    rep = settings.REP_STATUS[310]
                else:
                    rep = settings.REP_STATUS[100]

                    rep['data'] = dict(
                        userName=student.user_name,
                        stuId=student.stu_id,
                        school=student.school,
                        college=student.college,
                        mailbox=student.mailbox,
                        img=settings.DEFAULT_IMG,
                        token=student.token)
                    rep['data']['class'] = student.stu_class
            except KeyError:
                rep = settings.REP_STATUS[300]
            except Student.DoesNotExist:
                rep = settings.REP_STATUS[211]
            except AttributeError:
                rep = settings.REP_STATUS[200]
        else:
            rep = settings.REP_STATUS[666]
    else:
        rep = settings.REP_STATUS[111]
    return JsonResponse(rep, safe=False)


def date_fomat(date):
    return str(date).split('+')[0]
