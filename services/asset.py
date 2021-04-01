import json
import traceback
from datetime import timezone

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from common.models import Asset
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
from controller.handler import dispatcherBase


@require_http_methods(['GET'])
def listAsset(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    data = Asset.objects.values()
    page = request.GET.get('page')
    pagesize = request.GET.get('pagesize')
    # 使用分页对象，设定每页多少条记录
    pgnt = Paginator(data, pagesize)
    # 从数据库中读取数据，指定读取其中第几页
    currentData = pgnt.page(page)

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    assetList = list(currentData)
    return JsonResponse({'success': 'true', 'assetList': assetList, 'total': pgnt.count})


@require_http_methods(['GET'])
def findByJobNumber(request):
    job = request.GET.get('jobNumber')
    data = Asset.objects.filter(jobNumber=job)
    assetList = []
    for i in data.values():
        assetList.append(i)
    return JsonResponse({'success': 0, 'assetList': assetList}, safe=False)


@require_http_methods(['GET'])
def findByAssetNumber(request):
    asset = request.GET.get('assetNumber')
    data = Asset.objects.filter(assetNumber__contains=asset)
    assetList = []
    for i in data.values():
        assetList.append(i)
    return JsonResponse({'ret': 0, 'assetList': assetList}, safe=False)


@require_http_methods(['POST'])
def updateAsset(request):
    assetId = request.POST.get('id')
    asset = Asset.objects.get(id=assetId)
    if asset is None:
        return JsonResponse({
            'success': 'false',
            'msg': '资产信息不存在！'
        })
    else:
        asset.dateTime = timezone.now()
        asset.jobNumber = request.POST.get('jobNumber')
        asset.deviceName = request.POST.get('deviceName')
        asset.assetNumber = request.POST.get('assetNumber')
        asset.status = request.POST.get('status')
        asset.save()
        return JsonResponse({
            'success': 'true',
            'msg': '资产信息修改成功！'
        })


@require_http_methods(['POST'])
def deleteAsset(request):
    assetId = request.POST.get('id')
    try:
        asset = Asset.objects.get(id=assetId)
    except asset.DoesNotExist:
        return {
            'success': 'false',
            'msg': '用户不存在！'
        }
    asset.delete()
    return JsonResponse({
        'success': 'true',
        'msg': '删除资产信息成功！'
    })


@require_http_methods(['POST'])
def bathDeleteAsset(request):
    assetIds = request.POST.get('ids')
    ids = list(assetIds.split(','))
    for assetId in ids:
        if id != '':
            user = Asset.objects.get(id=assetId)
            user.delete()
    return JsonResponse({
        'ret': 0,
        'success': 'true',
        'msg': '资产信息删除成功！'
    })


ActionHandler = {
    'listAsset': listAsset,
    'findByJobNumber': findByJobNumber,
    'findByAssetNumber': findByAssetNumber,
    'updateAsset': updateAsset,
    'deleteAsset': deleteAsset,
    'bathDeleteAsset': bathDeleteAsset,
}


def dispatcher(request):
    return dispatcherBase(request)
