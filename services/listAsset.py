import json
import traceback
import time
import hashlib
import requests

from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from openpyxl.descriptors import Integer

from common.models import Asset
# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
from controller.handler import dispatcherBase


@require_http_methods(['GET'])
def listAsset(request):
    try:
        # 返回一个 QuerySet 对象 ，包含所有的表记录
        qs = Asset.objects.values()
        page = request.GET.get('page')
        pagesize = request.GET.get('pagesize')
        # 使用分页对象，设定每页多少条记录
        pgnt = Paginator(qs, pagesize)
        # 从数据库中读取数据，指定读取其中第几页
        currentPage = pgnt.page(page)
        # 将 QuerySet 对象 转化为 list 类型
        # 否则不能 被 转化为 JSON 字符串
        assetList = list(currentPage)
        return JsonResponse({'success': 'true', 'assetList': assetList, 'total': pgnt.count})
    except EmptyPage:
        return JsonResponse({'success': 'true', 'userList': [], 'total': 0})

    except:
        return JsonResponse({'success': 'false', 'msg': f'未知错误\n{traceback.format_exc()}'})


@require_http_methods(['GET'])
def listByStatus(request):
    assetStatus = request.GET.get('status')
    data = Asset.objects.get(status=assetStatus)
    qs = model_to_dict(data)
    result = [qs]
    # page = request.GET.get('page')
    # pagesize = request.GET.get('pagesize')
    # # 使用分页对象，设定每页多少条记录
    # pgnt = Paginator(qs, pagesize)
    # # 从数据库中读取数据，指定读取其中第几页
    # currentPage = pgnt.page(page)
    # assetList = list(currentPage)
    # assetList = model_to_dict(qs)
    return JsonResponse({'success': 'true', 'assetList': result}, safe=False)


@require_http_methods(['GET'])
def findByJobNumber(request):
    job = request.GET.get('jobNumber')
    assetList = model_to_dict(Asset.objects.get(jobNumber=job))
    return JsonResponse({'ret': 0, 'assetList': assetList}, safe=False)


@require_http_methods(['GET'])
def findByAssetNumber(request):
    asset = request.GET.get('assetNumber')
    assetList = model_to_dict(Asset.objects.get(assetNumber=asset))
    return JsonResponse({'ret': 0, 'assetList': assetList}, safe=False)


@require_http_methods(['POST'])
def addAsset(request):
    asset = Asset(dateTime=timezone.now(),
                  jobNumber=request.POST.get('jobNumber'),
                  deviceName=request.POST.get('deviceName'),
                  assetNumber=request.POST.get('assetNumber'),
                  status=request.POST.get('status'), )
    asset.save()
    return JsonResponse({
        'success': 'true',
        'msg': '资产信息添加成功！'
    })


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
            data = Asset.objects.get(id=assetId)
            data.delete()
    return JsonResponse({
        'ret': 0,
        'success': 'true',
        'msg': '资产信息删除成功！'
    })


@require_http_methods(['GET'])
def addToOa(request):
    assetIds = request.GET.get('ids')
    ids = list(assetIds.split(','))
    assets = {'assetNumber', 'jobNumber'}
    for assetId in ids:
        if id != '':
            data = Asset.objects.filter(id=assetId).values('jobNumber', 'assetNumber')
            for i in data.values():
                jobNumber0 = i['jobNumber']
                jobNumber = str(jobNumber0)
                assetNumber0 = i['assetNumber']
                assetNumber = assetNumber0.strip()
                listData = {assetNumber: jobNumber}
                print(listData)

    # appId = "qSymvYkZ4a2caQNVgKHG"
    # appSecret = "XchRcjaVQySxS8G2Vzf3CZamY7zxVWgJ"
    # interfaceId = "99f2ac375978e374557067455b855eab"
    appId = "qHSYjTfnh3MhXqBmnaWk"
    appSecret = "PWx4w9pa7UkPCZLAR6fXG9wJX2VHzgKQ"
    interfaceId = "203868a71f188ed965682ac5a904b469"
    timestamp = time.time()
    timestampToOa = int(round(timestamp * 10))
    timeStamp = str(round(timestamp * 10))
    str2 = "xqg59ijt"
    string = appId + appSecret + interfaceId + str2 + timeStamp
    # 生成OA资产修改接口的token
    md5 = hashlib.md5()
    md5.update(string.encode())
    tokenToOa = md5.hexdigest()

    # 新建字典
    param = {}
    oaData = {"type": "it_manager", "info": listData}
    param["data"] = oaData
    param["appId"] = appId
    param["nonce"] = str2
    param["timestamp"] = timestampToOa
    param["interfaceId"] = interfaceId
    param["token"] = tokenToOa
    print(param)
    # 转换成json数据格式
    jsonParam = json.dumps(param)
    print(jsonParam)
    oaUrl = "https://testqxflowprocess.37wan.com/api.php/taker/rouseInterface"
    re = requests.post(oaUrl, jsonParam)

    result = json.loads(re.text)

    return JsonResponse({
        'code': 0,
        'success': 'false',
        'data': result,
        'msg': 'msg'
    })


ActionHandler = {
    'listAsset': listAsset,
    'listByStatus': listByStatus,
    'updateAsset': updateAsset,
    'deleteAsset': deleteAsset,
    'addAsset': addAsset,
    'bathDeleteAsset': bathDeleteAsset,
    'findByJobNumber': findByJobNumber,
    'findByAssetNumber': findByAssetNumber,
    'addToOa': addToOa
}


def dispatcher(request):
    return dispatcherBase(request)
