import json
import random
import time
import hashlib
import requests

from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q

from common.models import Asset
from django.core.paginator import Paginator


def listAsset(request):
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


# 显示未录入系统的资产数据
def listByStatus(request):
    assetStatus = request.GET.get('status')
    data = Asset.objects.all().filter(status=assetStatus)
    dataList = []
    for i in data.values():
        dataList.append(i)
    page = request.GET.get('page')
    pagesize = request.GET.get('pagesize')
    # 使用分页对象，设定每页多少条记录
    pgnt = Paginator(dataList, pagesize)
    # 从数据库中读取数据，指定读取其中第几页
    currentData = pgnt.page(page)
    assetList = list(currentData)
    return JsonResponse({'success': 'true', 'assetList': assetList,
                         'size': pagesize, 'totalElements': pgnt.count,
                         'totalPages': pgnt.num_pages}, safe=False)


# class DateEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return obj.strftime("%Y-%m-%d %H:%M:%S")
#         else:
#             return json.JSONEncoder.default(self, obj)

# 根据工号查询资产信息
def findByJobNumber(request):
    job = request.GET.get('jobNumber')
    data = Asset.objects.filter(Q(jobNumber=job) & Q(status="否"))
    assetList = []
    for i in data.values():
        assetList.append(i)
    return JsonResponse({'assetList': assetList}, safe=False)


# 根据资产编号查询资产信息
def findByAssetNumber(request):
    asset = request.GET.get('assetNumber').strip()
    data = Asset.objects.filter(Q(assetNumber=asset) & Q(status="否"))
    assetList = []
    for i in data.values():
        assetList.append(i)
    return JsonResponse({'assetList': assetList}, safe=False)


# 新增资产信息
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


# 编辑资产信息
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


# 删除资产信息
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


# 批量删除资产信息
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


# 资产信息批量更新
def addToOa(request):
    # 获取入库资产信息的id
    assetIds = request.GET.get('ids')
    ids = list(assetIds.split(','))
    # 根据id获取资产信息的资产编号和工号，以字典的形式保存至assets
    assets = {}
    for assetId in ids:
        data = Asset.objects.filter(id=assetId).values('jobNumber', 'assetNumber')
        for i in data.values():
            jobNumber0 = i['jobNumber']
            jobNumber = str(jobNumber0)
            assetNumber0 = i['assetNumber']
            assetNumber = assetNumber0.strip()
            assets[assetNumber] = jobNumber
    print(assets)
    # 后台公用组件获取，用于接口处身份验证
    appId = "qSymvYkZ4a2caQNVgKHG"
    appSecret = "XchRcjaVQySxS8G2Vzf3CZamY7zxVWgJ"
    interfaceId = "99f2ac375978e374557067455b855eab"
    # 测试接口验证信息
    # appId = "qHSYjTfnh3MhXqBmnaWk"
    # appSecret = "PWx4w9pa7UkPCZLAR6fXG9wJX2VHzgKQ"
    # interfaceId = "203868a71f188ed965682ac5a904b469"
    timestamp = time.time()
    timestampToOa = int(round(timestamp * 10))
    timeStamp = str(round(timestamp * 10))
    str2 = generate_random_str(8)
    # 根据接口要求组成字符串，用于生成token
    string = appId + appSecret + interfaceId + str2 + timeStamp
    # 生成OA资产修改接口的token
    md5 = hashlib.md5()
    md5.update(string.encode())
    tokenToOa = md5.hexdigest()

    # 新建字典，保存提交到接口的参数数据
    param = {}
    oaData = {"type": "it_manager", "info": assets}
    param["data"] = oaData
    param["appId"] = appId
    param["nonce"] = str2
    param["timestamp"] = timestampToOa
    param["interfaceId"] = interfaceId
    param["token"] = tokenToOa
    # 转换成json数据格式
    jsonParam = json.dumps(param)
    print(jsonParam)
    # 测试接口
    # oaUrl = "https://testqxflowprocess.37wan.com/api.php/taker/rouseInterface"
    # 正式接口
    oaUrl = "http://eicommon.37wan.com/api.php/taker/rouseInterface"
    result = requests.post(oaUrl, jsonParam)

    # 将接口返回值转成json
    resultData = json.loads(result.text)
    print(resultData)

    return JsonResponse({'result': resultData})


# 生成一个指定长度的、由小写字母和数字组成的随机字符串
def generate_random_str(randomlength):
    random_str = ''
    base_str = 'abcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


# 入库成功后修改资产数据状态
def updateStatus(request):
    assetIds = request.POST.get('ids')
    ids = list(assetIds.split(','))
    for assetId in ids:
        asset = Asset.objects.get(id=assetId)
        asset.status = '是'
        asset.save()
    return JsonResponse({'success': 'true'})


# def dispatcher(request):
#     return dispatcherBase(request)
