from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
import hashlib
# from Seller import models
from Seller.models import *
from Buyer.models import *
from django.core.paginator import Paginator
from alipay import AliPay
from Qshop.settings import alipay_public_key_string, alipay_private_key_string


# Create your views here.


# 装饰器
def wrapper(func):
    def inner(request, *args, **kwargs):
        username1 = request.COOKIES.get('email')
        username2 = request.session.get('email')
        if username1 and username2 and username1 == username2:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/Buyer/login/')

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


## 商品列表
def goods_list(request):
    """
    req_type    完成判断请求
        当 req_type = search
            keywords 商品的名字
        当 req_type = showMore
            keywords传递的类型id，寻找该类型下面的商品
    :param request:
    :return:
    """
    keywords = request.GET.get("keywords")
    print(keywords)
    req_type = request.GET.get("req_type")
    print(req_type)
    if req_type == "showMore":
        # 查看更多
        goods_type = GoodsType.objects.get(id=keywords)
        goods = goods_type.goods_set.all()  ## 反向查询，
    elif req_type == "search":
        # 搜索功能
        goods = Goods.objects.filter(goods_name__contains=keywords).all()
        # print(goods)
    ## 从商品集中切片
    end = len(goods) // 5
    end += 1
    recommend = goods.order_by("goods_price")[:end]
    return render(request, "buyer/goods_list.html", locals())


def detail(request, id):
    goods = Goods.objects.get(id=int(id))

    return render(request, "buyer/detail.html", locals())


@wrapper
def user_center_info(request):
    return render(request, 'buyer/user_center_info.html', locals())


import time


## 订单页面
@wrapper
def place_order(request):
    ## 保存订单
    goods_id = request.GET.get("goods_id")  # 商品id
    goods_count = request.GET.get("goods_count")  ## 订单数量
    user_id = request.COOKIES.get("id")
    if goods_id and goods_count:
        goods_id = int(goods_id)
        goods_count = int(goods_count)
        goods = Goods.objects.get(id=goods_id)
        ## 保存订单表
        payorder = PayOrder()
        order_number = str(time.time()).replace('.', '')  ## 生产订单编号
        payorder.order_number = order_number  ## 订单编号
        payorder.order_status = 0
        payorder.order_total = goods.goods_price * goods_count
        payorder.order_user = LoginUser.objects.get(id=user_id)
        payorder.save()
        ## 保存订单详情表
        orderinfo = OrderInfo()
        orderinfo.order_id = payorder
        orderinfo.goods = goods
        orderinfo.goods_count = goods_count
        orderinfo.goods_price = goods.goods_price
        orderinfo.goods_total_price = goods.goods_price * goods_count
        orderinfo.store_id = goods.goods_store
        orderinfo.save()

        total_count = 0
        all_goods_info = payorder.orderinfo_set.all()
        for one in all_goods_info:
            total_count += one.goods_count

    return render(request, "buyer/place_order.html", locals())


def payViews(request):
    order_id = request.GET.get("order_id")  # 订单id
    payorder = PayOrder.objects.get(id=order_id)

    alipay = AliPay(  # 实例化支付对象
        appid='2016101300673929',
        app_notify_url=None,
        app_private_key_string=alipay_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
    )
    ## 实例化订单
    order_string = alipay.api_alipay_trade_page_pay(
        subject='天天生鲜',  ## 交易主题
        out_trade_no=payorder.order_number,  ## 订单号
        total_amount=str(payorder.order_total),  ## 交易总金额
        return_url="http://127.0.0.1:8000/Buyer/payResult/",  # 请求支付，之后及时回调的一个接口
        notify_url="http://127.0.0.1:8000/Buyer/payResult/"  # 通知地址，
    )
    ##   发送支付请求
    ## 请求地址  支付网关 + 实例化订单
    result = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return HttpResponseRedirect(result)


def payResult(request):
    order_number = request.GET.get("out_trade_no")
    payorder = PayOrder.objects.get(order_number=order_number)
    payorder.order_status = 1
    payorder.save()

    return render(request, "buyer/payResult.html", locals())


def cart(request):
    return render(request, 'buyer/cart.html', locals())


def user_center_order(request):
    return render(request, 'buyer/user_center_order.html', locals())


def user_center_site(request):
    return render(request, 'buyer/user_center_site.html', locals())
