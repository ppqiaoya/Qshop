from django.urls import path, re_path
from Buyer import views

urlpatterns = [

    path('register/', views.register),
    path('login/', views.login),
    path('index/', views.index),

    path('base/', views.base),
    path('logout/', views.logout),
    path('goods_list/', views.goods_list),
    path('user_center_info/', views.user_center_info),
    path('place_order/', views.place_order),
    path('place_order_more/', views.place_order_more),

    path('payViews/', views.payViews),
    path('payResult/', views.payResult),

    path('add_cart/', views.add_cart),

    path('cart/', views.cart),
    path('user_center_order/', views.user_center_order),
    path('user_center_site/', views.user_center_site),

    re_path('detail/(?P<id>\d+)', views.detail),

]
