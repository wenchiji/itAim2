from django.http import JsonResponse

from common.models import User


# 登录处理
from controller.handler import creatToken


def doLogin(request):
    # 从 HTTP 请求中获取用户名、密码参数
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({'success': 'false', 'msg': '用户不存在！'})

    if user and user.password == password:
        # 登录成功，生成token
        token = creatToken(user)
        return JsonResponse({'token': token, 'success': 'true', 'msg': '登录成功！'})
    else:
        return JsonResponse({'success': 'false', 'msg': '用户名或密码错误！'})


# 登出处理
# def logout(request):
#     # 使用登出方法
#     return JsonResponse({'ret': 0})
