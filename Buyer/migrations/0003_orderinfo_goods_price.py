# Generated by Django 2.2.1 on 2019-09-25 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0002_auto_20190925_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='goods_price',
            field=models.FileField(default=2, upload_to='', verbose_name='商品单价'),
            preserve_default=False,
        ),
    ]
