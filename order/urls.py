from django.conf.urls import url
from .views import order_place

urlpatterns = [
	url(r"^place/$", order_place, name="place") #订单提交页面

]