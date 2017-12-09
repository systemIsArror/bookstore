#encoding=utf-8
from django.conf.urls import url
from .views import order_place,order_commit

urlpatterns = [
	url(r"^place/$", order_place, name="place"), #订单提交页面
	url(r"^commit/$", order_commit, name="commit"), #生成订单
]