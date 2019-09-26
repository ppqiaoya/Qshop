from django.db import models
from Seller.models import *

# Create your models here.
class Consumer(models.Model):
    email=models.EmailField(verbose_name="")
    password=models.CharField(max_length=32)
    username=models.CharField(max_length=32,null=True,blank=True)
    phone=models.CharField(max_length=32,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    gender=models.CharField(max_length=4,null=True,blank=True)
    photo=models.ImageField(upload_to="images",null=True,blank=True)

    class Meta:
        db_table='consumer'

# 订单表
class PayOrder(models.Model):
    # 订单状态：
    # 0 未支付
    # 1 已支付
    # 2 待发货
    # 3 待收货
    # 4 完成
    # 5 拒收
    order_number = models.CharField(max_length=32,verbose_name="订单编号",unique=True)
    order_date = models.DateField(auto_now=True,verbose_name="订单日期")
    order_status = models.IntegerField(verbose_name="订单状态")
    order_total = models.FloatField(verbose_name="订单总价 ")
    order_user = models.ForeignKey(to= LoginUser,on_delete=models.CASCADE,verbose_name="订单用户")# 外键  链接到  用户表

    class Meta:
        db_table='payOrder'


# 订单详情表
class OrderInfo(models.Model):
    order_id = models.ForeignKey(to=PayOrder,on_delete=models.CASCADE,verbose_name="订单表外键")
    goods = models.ForeignKey(to=Goods,on_delete=models.CASCADE,verbose_name="商品表")
    goods_price=models.FloatField(verbose_name="商品单价")
    goods_count = models.IntegerField(verbose_name="商品数量")
    goods_total_price = models.FloatField(verbose_name="商品小计")
    store_id = models.ForeignKey(to=LoginUser,on_delete=models.CASCADE,verbose_name="店铺id")

    class Meta:
        db_table='orderInfo'
