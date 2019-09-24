from django.urls import path,re_path
from Seller import views

urlpatterns = [

    path('register/', views.register),
    path('login/', views.login),
    path('index/', views.index),
    path('logout/', views.logout),
    path('goods_add/', views.goods_add),

    path('goods_list/', views.goods_list),
    re_path('goods_list/(?P<status>[01])/(?P<page>\d+)',views.goods_list),
    re_path('goods_status/(?P<status>\w+)/(?P<id>\d+)',views.goods_status),


    path('personalInfo/', views.personalInfo),

]
