from django.conf.urls import url
from django.urls import path

from controller import login
from services import user, sign_in_out, listAsset, asset

urlpatterns = [
    path('login', login.doLogin),

    # 所有资产数据管理
    url(r'^allAsset/listAsset', asset.listAsset),
    url(r'^allAsset/findByJobNumber', asset.findByJobNumber),
    url(r'^allAsset/findByAssetNumber', asset.findByAssetNumber),
    url(r'^allAsset/updateAsset', asset.updateAsset),
    url(r'^allAsset/deleteAsset', asset.deleteAsset),
    url(r'^allAsset/bathDeleteAsset', asset.bathDeleteAsset),

    # 未入库资产数据管理
    url(r'^listAsset', listAsset.listAsset),
    url(r'^listByStatus', listAsset.listByStatus),
    url(r'^findByJobNumber', listAsset.findByJobNumber),
    url(r'^findByAssetNumber', listAsset.findByAssetNumber),
    url(r'^updateAsset', listAsset.updateAsset),
    url(r'^deleteAsset', listAsset.deleteAsset),
    url(r'^addAsset', listAsset.addAsset),
    url(r'^bathDeleteAsset', listAsset.bathDeleteAsset),
    url(r'^addToOa', listAsset.addToOa),
    url(r'^updateAssetStatus', listAsset.updateStatus),

    # 用户管理
    url(r'^listUser', user.listUser),
    url(r'^findByName', user.findByName),
    url(r'^addUser', user.addUser),
    url(r'^updateUser', user.editUser),
    url(r'^deleteUser', user.deleteUser),
    url(r'^bathDeleteUser', user.bathDeleteUser),

]
