#encoding:utf-8
from django.conf.urls import url
from .views import index,detail,b_list

urlpatterns = [
	url(r"^$",index, name='index'), #首页
	url(r"^list/(?P<type_id>\d+)/(?P<page>\d+)/$",b_list, name='list'), #图书列表
	url(r"^detail/(?P<books_id>\d+)/$", detail, name='detail'), #详情
]

