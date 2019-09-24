from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
import hashlib
# from Seller import models
from Seller.models import *
from Buyer.models import *
from django.core.paginator import Paginator


# Create your views here.


# 装饰器
def wrapper(func):
    def inner(request, *args, **kwargs):
        username1 = request.COOKIES.get('email')
        username2 = request.session.get('email')
        if username1 and username2 and username1 == username2:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('Buyer/login/')

    return inner


# 加密
def setmd5(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


# 注册
def register(request):
    if request.method == "POST":
        feedback = ''
        data = request.POST
        email = data.get('email')
        password1 = data.get('pwd')
        password2 = data.get('cpwd')
        if email and password1 and password2:
            if password1 != password2:
                feedback = '两次输入密码不相同'
            else:
                consumer = Consumer.objects.filter(email=email).first()
                if consumer and email == consumer.email:
                    feedback = '此账号已经注册,请直接登录'
                else:
                    consumer = Consumer()
                    consumer.email = email
                    consumer.password = setmd5(password1)
                    consumer.save()
                    feedback = '注册成功,去登录吧'
        else:
            feedback = '请填写所有信息进行注册'
    return render(request, 'buyer/register.html', locals())


# 登录
def login(request):
    if request.method == "POST":
        feedback = ''
        data = request.POST
        email = data.get('email')
        password = setmd5(data.get('pwd'))
        if email and password:
            consumer = Consumer.objects.filter(email=email).first()
            if consumer and email == consumer.email:
                if password and password == consumer.password:
                    response = HttpResponseRedirect('/Buyer/index/')
                    response.set_cookie('email', consumer.email)
                    response.set_cookie('id', consumer.id)
                    request.session['email'] = consumer.email
                    return response

                else:
                    feedback = '密码不对啊小老弟'
            else:
                feedback = '此账号不存在'
        else:
            feedback = '账号为空'

    return render(request, 'buyer/login.html', locals())


def base(request):
    return render(request, 'buyer/base.html', locals())


# @wrapper
# 首页
def index(request):
    goods_type = GoodsType.objects.all()
    result = []
    for type in goods_type:
        goods = type.goods_set.order_by("goods_price")
        if len(goods) >= 4:
            goods = goods[:4]
            result.append({"type": type, "goods": goods})

    return render(request, 'buyer/index.html', locals())


# 登出
def logout(request):
    response = HttpResponseRedirect('/Buyer/login/')
    keys = request.COOKIES.keys()
    for one in keys:
        response.delete_cookie(one)
    request.session.flush()
    return response


def goods_list(request):
    keywords = request.GET.get("keywords")

    goods_type = GoodsType.objects.get(id=keywords)

    goods = goods_type.goods_set.all()

    end = len(goods) // 5
    end += 1
    recommend = goods_type.goods_set.order_by("goods_price")[:end]

    # goods = Goods.objects.all()
    # recommend = Goods.objects.order_by("goods_price")
    return render(request, "buyer/goods_list.html", locals())
