from django.http import JsonResponse
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Admin, Student, Club
import jwt
from django.core.exceptions import PermissionDenied
# TODO
# 1. 信息展示模块
# 2. 学生端登陆注册


def auth_permission_required(perm, user_type='stu'):
    """
    token验证装饰器
    :param perm:
    :param user_type:
    :return:
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # 格式化权限
            perms = (perm,) if isinstance(perm, str) else perm

            if request.user.is_authenticated:
                # 正常登录用户判断是否有权限
                if not request.user.has_perms(perms):
                    raise PermissionDenied
            else:
                try:
                    auth = request.META.get('HTTP_AUTHORIZATION').split()
                except AttributeError:
                    return JsonResponse(settings.STATUS[210])

                # 用户通过API获取数据验证流程
                if auth[0].lower() == 'token':
                    try:
                        token = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
                        pho_num = token['data']['pho_num']
                    except jwt.ExpiredSignatureError:
                        return JsonResponse(settings.STATUS[110])
                    except jwt.InvalidTokenError:
                        return JsonResponse(settings.STATUS[101])

                    if user_type == 'stu':
                        try:
                            Student.objects.get(pho_num=pho_num)
                        except Student.DoesNotExist:
                            return JsonResponse(settings.STATUS[211])
                    elif user_type == 'admin':
                        try:
                            Admin.objects.get(pho_num=pho_num)
                        except Admin.DoesNotExist:
                            return JsonResponse(settings.STATUS[211])
                else:
                    return JsonResponse(settings.STATUS[210])
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


@csrf_exempt
def manager_register(request):
    """
    管理端注册
    :param request:
    :return:
    """
    if request.method == 'POST':
        post_body = request.body
        req_js = json.loads(post_body)
        print(req_js)
        if len(Admin.objects.filter(pho_num=req_js['phoNum'])):
            rep = settings.REP_STATUS[201]
        else:
            admin = Admin(
                user_name=req_js['userName'],
                pass_word=req_js['passWord'],
                shool=req_js['school'],
                stu_id=req_js['stuId'],
                pho_num=req_js['phoNum'])
            club = Club(
                club_name=req_js['clubName'],
                club_desc='',
                Admin=admin
            )
            admin.save()
            club.save()
            rep = settings.REP_STATUS[100]
            rep['data'] = dict(token=admin.token)
    else:
        rep = settings.REP_STATUS[111]
    return JsonResponse(rep, safe=False)


@csrf_exempt
def student_register(request):
    """
    学生端注册
    :param request:
    :return:
    """
    if request.method == 'POST':
        post_body = request.body
        req_js = json.loads(post_body)
        print(req_js)
        if len(Student.objects.filter(pho_num=req_js['phoNum'])):
            rep = settings.REP_STATUS[201]
        else:
            student = Student(
                user_name=req_js['userName'],
                stu_id=req_js['stuId'],
                shool=req_js['school'],
                college=req_js['college'],
                stu_class=req_js['class'],
                mailbox=req_js['mailbox'],
                pho_num=req_js['phoNum'],
                pass_word=req_js['passWord'],)
            student.save()
            rep = settings.REP_STATUS[100]
            rep['data'] = dict(token=student.token)
    else:
        rep = settings.REP_STATUS[111]
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
                user = Admin.objects.get(pho_num=req_js['phoNum'], pass_word=req_js['passWord'])
                rep = settings.REP_STATUS[100]
                rep['data'] = dict(token=user.token)
            except Admin.DoesNotExist:
                rep = settings.REP_STATUS[211]
            except AttributeError:
                rep = settings.REP_STATUS[200]
        elif lg_type == 1:
            try:
                user = Student.objects.get(pho_num=req_js['phoNum'], pass_word=req_js['passWord'])
                rep = settings.REP_STATUS[100]
                rep['data'] = dict(token=user.token)
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

