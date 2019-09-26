from django.db import models


# Create your models here.
class LoginUser(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=32)
    username = models.CharField(max_length=32, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=4, null=True, blank=True)
    photo = models.ImageField(upload_to="images", null=True, blank=True)

    class Meta:
        db_table = 'loginUser'


class GoodsType(models.Model):
    type_label = models.CharField(max_length=32)
    type_description = models.TextField()
    type_picture = models.ImageField(upload_to='images', default='images/03.jpg')


class Goods(models.Model):
    goods_number = models.CharField(max_length=11)
    goods_name = models.CharField(max_length=32)
    goods_price = models.DecimalField(max_digits=4, decimal_places=2)
    goods_location = models.CharField(max_length=32)
    goods_status = models.IntegerField(default=1)
    picture = models.ImageField(upload_to='images', default='images/03.jpg')
    goods_type = models.ForeignKey(to=GoodsType, on_delete=models.CASCADE, default=1)
    goods_store = models.ForeignKey(to=LoginUser, on_delete=models.CASCADE, default=1)
    goods_description=models.TextField(default="超级好吃!!!!!!!")

    class Meta:
        db_table = 'goods'
