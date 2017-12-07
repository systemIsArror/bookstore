#encoding=utf-8
from django.conf.urls import url
from .views import cart_add,cart_count,cart_show,cart_del

urlpatterns = [
	url(r'^add/$', cart_add, name='add'), #添加购物车数据
	url(r'^count/$', cart_count, name='count'), #获取用户购物车中商品的总额
	url(r"^$", cart_show, name='show'), #显示用户的购物车页面
	url(r"^del$", cart_del, name='delete'), #购物车商品记录删除

]