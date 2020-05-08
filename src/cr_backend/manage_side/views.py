from django.http import JsonResponse
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import User
import jwt
from django.core.exceptions import PermissionDenied
# TODO
# 1. 信息展示模块
# 2. 学生端登陆注册


def auth_permission_required(perm):
    """
    token验证装饰器
    :param perm:
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

                    try:
                        User.objects.get(pho_num=pho_num)
                    except User.DoesNotExist:
                        return JsonResponse(settings.STATUS[211])
                else:
                    return JsonResponse(settings.STATUS[210])
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


@csrf_exempt
def register(request):
    """
    注册，
    :param request:
    :return:
    """
    if request.method == 'POST':
        print("the POST method")
        post_body = request.body
        req_js = json.loads(post_body)
        print(req_js)
        if len(User.objects.filter(pho_num=req_js['phoNum'])):
            rep = settings.REP_STATUS[201]
        else:
            user = User(
                user_name=req_js['userName'],
                pass_word=req_js['passWord'],
                shool=req_js['school'],
                club_name=req_js['clubName'],
                stu_id=req_js['stuId'],
                pho_num=req_js['phoNum'])
            user.save()
            rep = settings.REP_STATUS[100]
    else:
        rep = settings.REP_STATUS[111]
    return JsonResponse(rep, safe=False)


@csrf_exempt
def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'POST':
        print("the POST method")
        post_body = request.body
        req_js = json.loads(post_body)
        print(req_js)
        try:
            user = User.objects.get(pho_num=req_js['phoNum'], pass_word=req_js['passWord'])
            rep = settings.REP_STATUS[100]
            rep['data'] = dict(token=user.token)
        except AttributeError:
            rep = settings.REP_STATUS[200]
    else:
        rep = settings.REP_STATUS[111]
    return JsonResponse(rep, safe=False)



