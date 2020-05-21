from django.http import JsonResponse
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Admin, Student, Club, Recruitment, Notice
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
                shool=req_js['school'],
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
                pass_word=req_js['passWord'],)
            student.save()
            rep = settings.REP_STATUS[100]
            rep['data'] = dict(token=student.token)
    except KeyError:
        rep = settings.REP_STATUS[300]
    return JsonResponse(rep, safe=False)


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


@csrf_exempt
def manager_login(request):
    """
    管理端登录
    :param request:
    :return:
    """
    return login(request, lg_type=0)


@csrf_exempt
def student_login(request):
    """
    用户端登录
    :param request:
    :return:
    """
    return login(request, lg_type=1)


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


@auth_permission_required()
def club_apply(request, user):
    if request.method == 'GET':
        clubs = Club.objects.filter(school=user.school)
        if len(clubs) == 0:
            rep = settings.REP_STATUS[301]
        else:
            rep = settings.REP_STATUS[100]
            rep['data'] = list()
            for club in clubs:
                club_data = dict()
                club_data['社团名'] = club.club_name
                club_data['社团简介'] = club.club_desc
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
