#encoding:utf-8
from django.conf.urls import url
from users.views import register,register_handle,user_login,login_handle,logout,user

urlpatterns = [
	url(r'^register/$',register,name='register'), #用户注册
	url(r'^login/$',user_login,name='login'), #用户登录
	url(r'^register_handle/$', register_handle, name='register_handle'), #用户注册处理
	url(r'^login_handle/$', login_handle, name='login_handle'), #用户注册处理
	url(r'^logout/$', logout, name='logout'), #用户注册处理
	url(r'^$', user, name='user'), #用户中心-信息页

]