from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


def creatToken(user):
    # drf-jwt中有通过user对象生成token的方法
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


def dispatcherBase(request):
    pass
    # 根据session判断用户是否是登录的管理员用户
    # if 'userType' not in request.session:
    #     return JsonResponse({
    #         'ret': 302,
    #         'msg': '用户未登录',
    #     },
    #         status=302)

