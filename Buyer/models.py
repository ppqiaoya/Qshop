from django.db import models

# Create your models here.
class Consumer(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=32)
    username=models.CharField(max_length=32,null=True,blank=True)
    phone=models.CharField(max_length=32,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    gender=models.CharField(max_length=4,null=True,blank=True)
    photo=models.ImageField(upload_to="images",null=True,blank=True)

    class Meta:
        db_table='consumer'