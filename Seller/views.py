from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
import hashlib
# from Seller import models
from Seller.models import *
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
            return HttpResponseRedirect('/Seller/login/')

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
        password1 = data.get('password1')
        password2 = data.get('password2')
        if email and password1 and password2:
            if password1 != password2:
                feedback = '两次输入密码不相同'
            else:
                loginuser = LoginUser.objects.filter(email=email).first()
                if loginuser and email == loginuser.email:
                    feedback = '此账号已经注册,请直接登录'
                else:
                    loginuser = LoginUser()
                    loginuser.email = email
                    loginuser.password = setmd5(password1)
                    loginuser.save()
                    feedback = '注册成功,去登录吧'
        else:
            feedback = '请填写所有信息进行注册'
    return render(request, 'seller/register.html', locals())


# 登录
def login(request):
    if request.method == "POST":
        feedback = ''
        data = request.POST
        email = data.get('email')
        password = setmd5(data.get('password'))
        if email and password:
            loginuser = LoginUser.objects.filter(email=email).first()
            if loginuser and email == loginuser.email:
                if password and password == loginuser.password:
                    response = HttpResponseRedirect('/Seller/index/')
                    response.set_cookie('email', loginuser.email)
                    response.set_cookie('id', loginuser.id)

                    request.session['email'] = loginuser.email
                    return response

                else:
                    feedback = '密码不对啊小老弟'
            else:
                feedback = '此账号不存在'
        else:
            feedback = '账号为空'

    return render(request, 'seller/login.html', locals())


@wrapper
# 首页
def index(request):
    return render(request, 'seller/index.html',locals())


# 登出
def logout(request):
    response = HttpResponseRedirect('/Seller/login/')
    keys = request.COOKIES.keys()
    for one in keys:
        response.delete_cookie(one)
    request.session.flush()
    return response


# 商品列表
def goods_list(request, status, page=1):
    page = int(page)
    if status == '0':
        goods_obj = Goods.objects.filter(goods_status=0).order_by('goods_number')
    else:
        goods_obj = Goods.objects.filter(goods_status=1).order_by('goods_number')
    goods_all = Paginator(goods_obj, 10)
    goods_list = goods_all.page(page)
    current_page = goods_list.number
    start = current_page - 3
    if start < 1:
        start = 0

    end = current_page + 2
    if end > goods_all.num_pages:
        end = goods_all.num_pages
    if start == 0:
        end = 5
    if end == goods_all.num_pages:
        start = goods_all.num_pages - 5
        if start < 1:
            start = 0
    page_range = goods_all.page_range[start:end]
    # 普通goods_list
    return render(request, 'seller/goods_list.html', locals())

    # vue调用goods_list
    # return render(request,'vue_goods_list.html')


# 上架下架
def goods_status(request,status,id):
    """
    完成当 下架  修改 status 为 0
    当 上架的   修改status 为 1
    :param request:
    :param status:  操作内容  up 上架    down   下架
     :param id:  商品id
    :return:
    """
    id = int(id)
    goods = Goods.objects.get(id=id)
    if status== "up":
        # 上架
        goods.goods_status = 1
    else:
        # 下架
        goods.goods_status = 0
    goods.save()

    ##  获取请求来源
    url =request.META.get("HTTP_REFERER","/Seller/goods_list/1/1/")
    return HttpResponseRedirect(url)


# 个人中心
@wrapper
def personalInfo(request):
        user_id = request.COOKIES.get("id")
        print(user_id)
        user = LoginUser.objects.filter(id=user_id).first()
        if request.method == "POST":
            ## 获取 数据，保存数据
            data = request.POST
            user.username = data.get("username")
            user.phone = data.get("phone")
            user.age = data.get("age")
            user.gender = data.get("gender")
            user.photo = request.FILES.get("photo")
            user.save()

        return render(request,'seller/personalInfo.html',locals())


# 商品信息录入
@wrapper
def goods_add(request):
    ###  处理post请求，获取数据，保存数据，返回响应
    goods_type = GoodsType.objects.all()
    if request.method == "POST":
        data = request.POST
        goods = Goods()
        goods.goods_number = data.get("goods_number")
        goods.goods_name = data.get("goods_name")
        goods.goods_price = data.get("goods_price")
        goods.goods_location = data.get("goods_location")
        goods.picture = request.FILES.get("picture")
        goods.save()
        goods_type = request.POST.get("goods_type")   # select 标签的value  类型是 string


        goods.goods_type = GoodsType.objects.get(id = goods_type)  # 保存类型

        # 保存店铺从cookie中获取到用户信息

        user_id = request.COOKIES.get("id")
        goods.goods_store = LoginUser.objects.get(id = user_id)
        goods.save()
    return render(request,"seller/goods_add.html",locals())


