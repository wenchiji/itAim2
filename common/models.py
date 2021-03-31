from django.db import models


# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class Asset(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    dateTime = models.DateTimeField(max_length=6, db_column='DateTime')
    jobNumber = models.IntegerField(db_column='JobNumber')
    deviceName = models.CharField(max_length=64, db_column='DeviceName')
    assetNumber = models.CharField(max_length=64, db_column='AssetNumber')
    status = models.CharField(max_length=4)

    class Meta:
        db_table = "AIM_assetsrelatedstatement"
