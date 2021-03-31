import sys

from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from common.models import User


# 登录处理
def doLogin(request):
    # 从 HTTP 请求中获取用户名、密码参数
    username = request.POST.get('username')
    password = request.POST.get('password')

    print(username, password)
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({'success': 'false', 'msg': '用户不存在！'})

    # 使用 Django auth 库里面的 方法校验用户名、密码
    # user = authenticate(username=username, password=password)

    if user and user.password == password:
        # 登录成功，生成token
        # drf-jwt中有通过user对象生成token的方法
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return JsonResponse({'token': token, 'success': 'true', 'msg': '登录成功！'})
    else:
        return JsonResponse({'success': 'false', 'msg': '用户名或密码错误！'})


# 登出处理
def logout(request):
    # 使用登出方法
    logout(request)
    return JsonResponse({'ret': 0})
