#encoding=utf-8
from django.conf.urls import url
from .views import order_place,order_commit,order_pay,check_pay

urlpatterns = [
	url(r"^place/$", order_place, name="place"), #订单提交页面
	url(r"^commit/$", order_commit, name="commit"), #生成订单
	url(r"^pay/$", order_pay, name="pay"), #订单支付
	url(r"^check_pay/$", check_pay, name="check_pay"), #查询支付结果

]