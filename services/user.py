import json
import traceback

from django.core import serializers
from django.forms import model_to_dict
from django.http import JsonResponse
from django.template.defaultfilters import safe
from django.views.decorators.http import require_http_methods

from common import models
from common.models import User
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
from controller.handler import dispatcherBase


@require_http_methods(['GET'])
def listUser(request):
    try:
        # 返回一个 QuerySet 对象 ，包含所有的表记录
        qs = User.objects.values()

        page = request.GET.get('page')
        pagesize = request.GET.get('pagesize')
        # 使用分页对象，设定每页多少条记录
        pgnt = Paginator(qs, pagesize)
        # 从数据库中读取数据，指定读取其中第几页
        currentPage = pgnt.page(page)
        # 将 QuerySet 对象 转化为 list 类型
        # 否则不能 被 转化为 JSON 字符串
        userList = list(currentPage)

        return JsonResponse({'ret': 0, 'userList': userList, 'total': pgnt.count})

    except EmptyPage:
        return JsonResponse({'ret': 0, 'userList': [], 'total': 0})

    except:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})


@require_http_methods(['GET'])
def findByName(request):
    # try:
    name = request.GET.get('username')
    # qs = User.objects.filter(username=name).values_list()
    # qs = User.objects.filter(username__contains=name).all()
    # userList = serializers.serialize("json", qs)
    # # userList = list(qs)
    # return JsonResponse({'userList': userList})
    userList = model_to_dict(User.objects.get(username__contains=name))
    return JsonResponse({'ret': 0, 'userList': userList}, safe=False)


# except EmptyPage:
#     return JsonResponse({'ret': 0, 'userList': [], 'total': 0})
#
# except:
#     return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})


@require_http_methods(['POST'])
def addUser(request):
    user = User(username=request.POST.get('username'),
                phone=request.POST.get('phone'),
                password=request.POST.get('password'))
    user.save()

    return JsonResponse({
        'success': 'true',
        'msg': '用户添加成功！'
    })


@require_http_methods(['POST'])
def editUser(request):
    userId = request.POST.get('id')
    user = User.objects.get(id=userId)
    if user is None:
        return JsonResponse({
            'success': 'false',
            'msg': '用户不存在！'
        })
    else:
        user.username = request.POST.get('username')
        user.phone = request.POST.get('phone')
        user.password = request.POST.get('password')
        user.save()
        return JsonResponse({
            'success': 'true',
            'msg': '用户信息修改成功！'
        })


@require_http_methods(['POST'])
def deleteUser(request):
    userId = request.POST.get('id')
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        return {
            'ret': 1,
            'success': 'false',
            'msg': '用户不存在！'
        }
    user.delete()
    return JsonResponse({
        'ret': 0,
        'success': 'true',
        'msg': '删除用户成功！'
    })


@require_http_methods(['POST'])
def bathDeleteUser(request):
    userIds = request.POST.get('ids')
    ids = list(userIds.split(','))
    for userId in ids:
        if id != '':
            user = User.objects.get(id=userId)
            user.delete()
    return JsonResponse({
        'ret': 0,
        'success': 'true',
        'msg': '删除用户成功！'
    })


ActionHandler = {
    'listUser': listUser,
    'findByName': findByName,
    'addUser': addUser,
    'editUser': editUser,
    'deleteUser': deleteUser,
    'bathDeleteUser': bathDeleteUser
}


def dispatcher(request):
    return dispatcherBase(request)
