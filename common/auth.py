import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_decode_handler


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
