import jwt
from django.http import JsonResponse
import json

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication, BaseJSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_decode_handler


def dispatcherBase(request):
    pass
    # 根据session判断用户是否是登录的管理员用户
    # if 'userType' not in request.session:
    #     return JsonResponse({
    #         'ret': 302,
    #         'msg': '用户未登录',
    #         # 'redirect': '/mgr/sign.html'
    #     },
    #         status=302)
    #
    # if request.session['userType'] != 'mgr':
    #     return JsonResponse({
    #         'ret': 302,
    #         'msg': '用户非mgr类型',
    #         # 'redirect': '/mgr/sign.html'
    #     },
    #         status=302)


def options(self, request, *args, **kwargs):
    method = request.META.get('Access-Control-Allow-Method')
    origin = request.META.get('Origin')

# class Dispatcher(APIVIEW):
#     authentication_classes = [JSONWebTokenAuthentication, ]
#     permission_classes = [IsAuthenticated, ]
#
#     def get(self, request):
#         print(request.user)
#         return Response('数据')


class JwtAuthentication(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_Authorization'.upper())
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('过期了')
        except jwt.DecodeError:
            raise AuthenticationFailed('解码错误')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('不合法的token')
        # 得到的user对象，应该是自己user表的user对象
        print(payload)
        # user=MyUser.objects.get(id=payload['user_id'])
        user = payload

        return user, token
