from django.forms import model_to_dict
from django.http import JsonResponse
from django.template.defaultfilters import safe
from django.views.decorators.http import require_http_methods

from common.models import User
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
from controller.handler import dispatcherBase


def listUser(request):
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
    return JsonResponse({'success': 'true', 'userList': userList,
                         'size': pagesize, 'totalElements': pgnt.count,
                         'totalPages': pgnt.num_pages})


def findByName(request):
    name = request.GET.get('username')
    if name:
        user = User.objects.get(username__contains=name)
        users = model_to_dict(user)
        userList = [users]
    else:
        users = User.objects.values()
        userList = list(users)
    return JsonResponse({'userList': userList}, safe=False)


def addUser(request):
    aa = User.objects.filter(username=request.POST.get('username'))
    if aa.exists():
        return JsonResponse({
            'success': 'false',
            'msg': '用户已存在！'
        })
    else:
        user = User(username=request.POST.get('username'),
                    phone=request.POST.get('phone'),
                    password=request.POST.get('password'))
        user.save()
        return JsonResponse({
            'success': 'true',
            'msg': '用户添加成功！'
        })


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
