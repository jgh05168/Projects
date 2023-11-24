from django.db import models


# Create your models here.

class Bank(models.Model):
    name = models.CharField(max_length=250, unique=True)


# 예금 상품 모델
class DepositProduct(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    dcls_month = models.IntegerField(blank=True, null=True)
    fin_prdt_cd = models.TextField(blank=True, null=True)
    fin_prdt_nm = models.TextField(blank=True, null=True)
    kor_co_nm = models.TextField(blank=True, null=True)
    dcls_strt_day = models.IntegerField(blank=True, null=True)
    dcls_end_day = models.IntegerField(blank=True, null=True)
    join_deny = models.IntegerField(blank=True, null=True)
    join_way = models.TextField(blank=True, null=True)
    spcl_cnd = models.TextField(blank=True, null=True)

class Deposit(models.Model):
    deposit_product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE)
    intr_rate = models.FloatField(blank=True, null=True)
    save_trm = models.IntegerField(blank=True, null=True)
    intr_rate_type = models.TextField(blank=True, null=True)
    intr_rate_type_nm = models.TextField(blank=True, null=True)
    intr_rate2 = models.FloatField(blank=True, null=True)


# 적금 상품 모델
class SavingProduct(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    dcls_month = models.IntegerField(blank=True, null=True)
    fin_prdt_cd = models.TextField(blank=True, null=True)
    fin_prdt_nm = models.TextField(blank=True, null=True)
    kor_co_nm = models.TextField(blank=True, null=True)
    dcls_strt_day = models.IntegerField(blank=True, null=True)
    dcls_end_day = models.IntegerField(blank=True, null=True)
    join_deny = models.IntegerField(blank=True, null=True)
    join_way = models.TextField(blank=True, null=True)
    spcl_cnd = models.TextField(blank=True, null=True)


class Saving(models.Model):
    saving_product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE)
    intr_rate = models.FloatField(blank=True, null=True)
    save_trm = models.IntegerField(blank=True, null=True)
    intr_rate_type = models.TextField(blank=True, null=True)
    intr_rate_type_nm = models.TextField(blank=True, null=True)
    intr_rate2 = models.FloatField(blank=True, null=True)
    rsrv_type = models.TextField(blank=True, null=True)
    rsrv_type_nm = models.TextField(blank=True, null=True)


