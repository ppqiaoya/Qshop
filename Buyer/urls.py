from django.urls import path
from Buyer import views

urlpatterns = [

    path('register/', views.register),
    path('login/', views.login),
    path('index/', views.index),

    path('base/', views.base),
    path('logout/', views.logout),
    path('goods_list/', views.goods_list),

]
