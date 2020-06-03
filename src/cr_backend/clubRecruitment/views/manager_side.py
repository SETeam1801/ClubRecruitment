#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import (absolute_import, unicode_literals)
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from ..models import Admin, Student, Club, Recruitment, Notice, Department, Img
from .general import auth_permission_required, post_log, login, send, date_fomat
import time


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
def add_club_info(_request, req_js, user):
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
def find_apps(request, _admin, dept_id):
    if request.method == 'GET':
        try:
            dept = Department.objects.get(pk=dept_id)
            apps = Recruitment.objects.filter(Department=dept)
            apps = [app for app in apps if app.stu_status >= 0]
            if len(apps) == 0:
                rep = settings.REP_STATUS[301]
            else:
                rep = settings.REP_STATUS[100]
                rep['data'] = dict()
                rep['data']['students'] = list()
                rep['data']['status'] = apps[0].stu_status
                for app in apps:
                    app_data = dict()
                    app_data['id'] = app.pk
                    app_data['stuName'] = app.stu_name
                    stu = app.Student
                    app_data['img'] = stu.avatar
                    app_data['status'] = app.stu_status
                    rep['data']['students'].append(app_data)
                rep['data']['students'].sort(key=lambda x: (x.get('status', 0)), reverse=True)
                rep['data']['round'] = dept.current_round
                rep['data']['stuNum'] = len(apps)
                rep['data']['passNum'] = len([app for app in apps if app.stu_status != 0])
                rep['data']['deleteNum'] = len([app for app in apps if app.stu_status == 0])
        except Department.DoesNotExist:
            rep = settings.REP_STATUS[211]
    else:
        rep = settings.REP_STATUS[111]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
@post_log
def edit_notice(_request, req_js, admin):
    """
    编辑通知
    :param _request:
    :param req_js:
    :param admin:
    :return:
    """
    try:
        club = Club.objects.get(Admin=admin)
        dept = Department.objects.get(pk=req_js['deptId'])
        for status in ['pass', "fail"]:
            for stu_id in req_js[status]['list']:
                stu = Student.objects.get(pk=stu_id)
                notice = Notice(
                    text=req_js[status]['text'],
                    title=req_js[status]['title'],
                    date=req_js[status]['date'],
                    Club=club,
                    Department=dept,
                    Student=stu
                )
                notice.save()
        rep = settings.REP_STATUS[100]
    except KeyError:
        rep = settings.REP_STATUS[300]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
@post_log
def add_dept(_request, req_js, admin):
    """
    增加部门
    :param _request:
    :param req_js:
    :param admin:
    :return:
    """
    try:
        club = Club.objects.get(Admin=admin)
        assert len(Department.objects.filter(dept_name=req_js['deptName'])) == 0
        dept = Department(
            Club=club,
            dept_name=req_js['deptName'],
            dept_desc=req_js['deptDesc']
        )
        dept.save()
        rep = settings.REP_STATUS[100]
    except KeyError:
        rep = settings.REP_STATUS[300]
    except AssertionError:
        rep = settings.REP_STATUS[400]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
@post_log
def delete_dept(_request, req_js, _admin):
    """
    删除部门
    :param _request:
    :param req_js:
    :param _admin:
    :return:
    """
    try:
        Department.objects.get(dept_name=req_js['deptName']).delete()
        rep = settings.REP_STATUS[100]
    except KeyError:
        rep = settings.REP_STATUS[300]
    except Department.DoesNotExist:
        rep = settings.REP_STATUS[211]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
def find_depts(_request, admin):
    try:
        club = Club.objects.get(Admin=admin)
        depts = Department.objects.filter(Club=club)
        assert len(depts) > 0
        rep = settings.REP_STATUS[100]
        rep['data'] = list()
        for dept in depts:
            dept_dic = dict()
            dept_dic['deptId'] = dept.pk
            dept_dic['deptName'] = dept.dept_name
            dept_dic['status'] = dept.status
            rep['data'].append(dept_dic)
    except KeyError:
        rep = settings.REP_STATUS[300]
    except Department.DoesNotExist:
        rep = settings.REP_STATUS[211]
    except AssertionError:
        rep = settings.REP_STATUS[100]
        rep['data'] = list()
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
@post_log
def edit_recruitment(_request, req_js, _admin):
    try:
        dept = Department.objects.get(pk=req_js['deptId'])
        dept.start_time = req_js['startTime']
        dept.end_time = req_js['endTime']
        s_time = time.mktime(time.strptime(dept.start_time, '%Y-%m-%d %H:%M:%S'))
        e_time = time.mktime(time.strptime(dept.end_time, '%Y-%m-%d %H:%M:%S'))
        assert s_time < e_time and time.time() < e_time   # 防止时间错误
        dept.qq = req_js['qq']
        dept.times = req_js['times']
        dept.max_num = req_js['maxNum']
        dept.recruit_num = req_js['recruitNum']
        dept.standard = req_js['standard']
        dept.add = req_js['add']
        dept.status = 1
        dept.save()
        rep = settings.REP_STATUS[100]
    except KeyError:
        rep = settings.REP_STATUS[300]
    except Department.DoesNotExist:
        rep = settings.REP_STATUS[211]
    except AssertionError:
        rep = settings.REP_STATUS[311]
    return JsonResponse(rep, safe=False)

#
# @csrf_exempt
# @auth_permission_required(user_type='admin')
# def edit_recruitment(_request, admin):
#     try:
#
#         dept = Department.objects.get(pk=req_js['deptId'])
#         dept.start_time = req_js['startTime']
#         dept.end_time = req_js['endTime']
#         s_time = time.mktime(time.strptime(dept.start_time, '%Y-%m-%d %H:%M:%S'))
#         e_time = time.mktime(time.strptime(dept.end_time, '%Y-%m-%d %H:%M:%S'))
#         assert s_time < e_time  # 防止时间错误
#         dept.qq = req_js['qq']
#         dept.times = req_js['times']
#         dept.max_num = req_js['maxNum']
#         dept.recruit_num = req_js['recruitNum']
#         dept.standard = req_js['standard']
#         dept.add = req_js['add']
#         dept.status = 1
#         dept.save()
#         rep = settings.REP_STATUS[100]
#     except KeyError:
#         rep = settings.REP_STATUS[300]
#     except Department.DoesNotExist:
#         rep = settings.REP_STATUS[211]
#     except AssertionError:
#         rep = settings.REP_STATUS[311]
#     return JsonResponse(rep, safe=False)



@csrf_exempt
@auth_permission_required(user_type='admin')
def upload_img(request, admin):
    if request.method == 'POST':
        avatar = request.FILES.get('img')
        img = Img(url=avatar)
        img.save()
        rep = settings.REP_STATUS[100]
        rep['url'] = settings.WEB_PATH + img.url.name
        club = Club.objects.get(Admin=admin)
        if club.place == 0:
            club.img0 = rep['url']
        elif club.place == 1:
            club.img1 = rep['url']
        elif club.place == 2:
            club.img2 = rep['url']
        elif club.place == 3:
            club.img3 = rep['url']
        elif club.place == 4:
            club.img4 = rep['url']
        club.place = (club.place + 1) % 5
        club.save()
    else:
        rep = settings.REP_STATUS[111]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
def delete_img(request, admin, img_id):
    if request.method == 'GET':
        club = Club.objects.get(Admin=admin)
        if img_id == 0:
            club.img0 = ''
        elif img_id == 1:
            club.img1 = ''
        elif img_id == 2:
            club.img2 = ''
        elif img_id == 3:
            club.img3 = ''
        elif img_id == 4:
            club.img4 = ''
        club.save()
        rep = settings.REP_STATUS[100]
    else:
        rep = settings.REP_STATUS[111]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
@post_log
def send_mails(_request, req_js, _admin):
    try:
        apps = Recruitment.objects.filter(pk=req_js['deptId'])
        fail_num = 0
        for app in [app for app in apps if app.stu_status >= 0]:
            try:
                send(req_js['passTitle'], app.stu_name + "同学:\n" + req_js['passBody'] + '\n\n' +
                     time.asctime(time.localtime(time.time())), [app.mailbox])
            except Exception:
                fail_num += 1
        for app in [app for app in apps if app.stu_status == 0]:
            try:
                send(req_js['failTitle'], app.stu_name + "同学:\n" + req_js['failBody'] + '\n\n' +
                     time.asctime(time.localtime(time.time())), [app.mailbox])
                app.stu_status = -1
                app.save()
            except Exception:
                fail_num += 1
        rep = settings.REP_STATUS[100]
        if fail_num:
            rep['data'] = dict(failNum=fail_num)
    except Student.DoesNotExist:
        rep = settings.REP_STATUS[211]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
def club_info(_request, admin):
    try:
        club = Club.objects.get(Admin=admin)
        depts = Department.objects.filter(Club=club)
        rep = settings.REP_STATUS[100]
        rep['data'] = dict()
        rep['data']['clubName'] = club.club_name
        rep['data']['clubDesc'] = club.club_desc
        rep['data']['clubPictureUrl'] = list()
        if club.img0 != '':
            rep['data']['clubPictureUrl'].append(club.img0)
        else:
            rep['data']['clubPictureUrl'].append(settings.DEFAULT_IMG)
        if club.img1 != '':
            rep['data']['clubPictureUrl'].append(club.img1)
        else:
            rep['data']['clubPictureUrl'].append(settings.DEFAULT_IMG)
        if club.img2 != '':
            rep['data']['clubPictureUrl'].append(club.img2)
        else:
            rep['data']['clubPictureUrl'].append(settings.DEFAULT_IMG)
        if club.img3 != '':
            rep['data']['clubPictureUrl'].append(club.img3)
        else:
            rep['data']['clubPictureUrl'].append(settings.DEFAULT_IMG)
        if club.img4 != '':
            rep['data']['clubPictureUrl'].append(club.img4)
        else:
            rep['data']['clubPictureUrl'].append(settings.DEFAULT_IMG)
        rep['data']['dept'] = list()
        for dept in depts:
            dept_dic = dict()
            dept_dic['deptId'] = dept.pk
            dept_dic['deptDesc'] = dept.dept_desc
            dept_dic['deptName'] = dept.dept_name
            dept_dic['status'] = dept.status
            dept_dic['recruitment'] = dict()
            dept_dic['recruitment']["startTime"] = date_fomat(dept.start_time)
            dept_dic['recruitment']["endTime"] = date_fomat(dept.end_time)
            dept_dic['recruitment']["deptId"] = dept.pk
            dept_dic['recruitment']["qq"] = dept.qq
            dept_dic['recruitment']["times"] = dept.times
            dept_dic['recruitment']["maxNum"] = dept.max_num
            dept_dic['recruitment']["recruitNum"] = dept.recruit_num
            dept_dic['recruitment']["standard"] = dept.standard
            dept_dic['recruitment']["add"] = dept.add
            rep['data']['dept'].append(dept_dic)
    except KeyError:
        rep = settings.REP_STATUS[300]
    except Club.DoesNotExist:
        rep = settings.REP_STATUS[211]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
def stu_info(request, _admin, app_id):
    if request.method == 'GET':
        try:
            app = Recruitment.objects.get(pk=app_id)
            dept = app.Department
            rep = settings.REP_STATUS[100]
            rep['data'] = dict()
            rep['data']['stuName'] = app.stu_name
            rep['data']['stuId'] = app.stu_id
            rep['data']['deptName'] = dept.dept_name
            rep['data']['phoNum'] = app.pho_num
            rep['data']['mailbox'] = app.mailbox
            rep['data']['stuDesc'] = app.stu_desc
        except Recruitment.DoesNotExist:
            rep = settings.REP_STATUS[211]
    else:
        rep = settings.REP_STATUS[111]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
def next_round(request, _admin, dept_id):
    if request.method == 'GET':
        try:
            dept = Department.objects.get(pk=dept_id)
            dept.current_round += 1
            if dept.current_round > dept.times:
                apps = Recruitment.objects.filter(Department=dept)
                for app in apps:
                    if app.stu_status != 0:
                        app.stu_status = 2
                        app.save()
            assert dept.current_round != dept.times+2
            dept.save()
            rep = settings.REP_STATUS[100]
        except Department.DoesNotExist:
            rep = settings.REP_STATUS[211]
        except AssertionError:
            rep = settings.REP_STATUS[301]
    else:
        rep = settings.REP_STATUS[111]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
@post_log
def stop_apply(_request, req_js, _admin):
    try:
        for app_id in req_js['stopList']:
            app = Recruitment.objects.get(pk=app_id)
            app.stu_status = 0
            app.save()
        rep = settings.REP_STATUS[100]
    except KeyError:
        rep = settings.REP_STATUS[300]
    except Recruitment.DoesNotExist:
        rep = settings.REP_STATUS[211]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
@post_log
def delete_apply(_request, req_js, _admin):
    try:
        for app_id in req_js['deleteList']:
            Recruitment.objects.get(pk=app_id).delete()
        rep = settings.REP_STATUS[100]
    except KeyError:
        rep = settings.REP_STATUS[300]
    except Recruitment.DoesNotExist:
        rep = settings.REP_STATUS[211]
    return JsonResponse(rep, safe=False)


@csrf_exempt
@auth_permission_required(user_type='admin')
@post_log
def change_dept_info(_request, req_js, _admin):
    try:
        dept = Department.objects.get(dept_name=req_js['pastName'])
        dept.dept_name = req_js['newName']
        dept.dept_desc = req_js['deptDesc']
        dept.save()
        rep = settings.REP_STATUS[100]
    except KeyError:
        rep = settings.REP_STATUS[300]
    except Department.DoesNotExist or Recruitment.DoesNotExist:
        rep = settings.REP_STATUS[211]
    return JsonResponse(rep, safe=False)


