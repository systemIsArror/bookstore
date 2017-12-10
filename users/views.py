#encoding:utf-8
from django.http import JsonResponse
from django.shortcuts import render,redirect
import re
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from order.models import OrderInfo, OrderGoods
from .models import Passport,Address
from utils.decorators import login_required

# Create your views here.
def register(request):
	return render(request,'users/register.html')

def register_handle(request):
	'''用户注册'''
	username = request.POST.get('user_name')
	password = request.POST.get('pwd')
	email = request.POST.get('email')

	if not all([username,password,email]):
		#有数据为空
		return render(request,'users/register.html',{"errormsg":"参数不能为空！"})
	#判断邮箱是否合法
	if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
		return render(request,'users/register.html',{'errormsg':'邮箱格式不对！'})

	p = Passport.objects.check_passport(username=username)
	if p:
		return render(request, 'users/register.html', {"errmsg": "用户名已经存在"})
	#向数据库中插入数据
	Passport.objects.add_one_passport(username=username,password=password,email=email)
	return redirect(reverse('user:login'))

def user_login(request):
	return render(request, 'users/login.html')

@csrf_exempt
def login_handle(request):
	'''进行用户登录验证'''
	username = request.POST.get("username")
	password = request.POST.get("password")
	remember = request.POST.get("remember")
	print(username)
	print(password)
	if not all([username,password]):
		return JsonResponse({"res": 2})

	passport = Passport.objects.get_one_passport(username=username, password=password)
	if passport:
		next_url = request.session.get("url_path",reverse("books:index"))

		jres = JsonResponse({"res":1, 'next_url':next_url})
		if remember == 'true':
			#记住用户名
			jres.set_cookie('username',username,max_age=7*24*3600)
		else:
			#不需要记住用户名
			jres.delete_cookie("username")

		request.session["islogin"] = True
		request.session["username"] = username
		request.session["passport_id"] = passport.id
		return jres
	#用户名或密码错误
	return JsonResponse({"res": 0})

def logout(request):
	'''注销'''
	#清楚当前用户的session信息
	request.session.flush()
	# del request.session["username"]
	return redirect(reverse('books:index', ))

@login_required
def user(request):
	'''用户中心——信息页'''
	passport_id = request.session.get("passport_id")
	#获取用户的基本信息
	addr = Address.objects.get_default_address(passport_id=passport_id)

	books_li = []

	context = {
		'addr': addr,
		'page': 'user',
		'book_li': books_li
	}
	return render(request, 'users/user_center_info.html', context)

@login_required
def address(request):
	'''用户中心--地址页'''
	#获取登录用户的id
	passport_id = request.session.get("passport_id")

	if request.method == "GET":
		#显示地址页面
		#查询用户的默认地址
		addr = Address.objects.get_default_address(passport_id=passport_id)
		other_addr = Address.objects.get_other_address(passport_id=passport_id)
		return render(request, "users/user_center_site.html", {"addr": addr, "page": "address", "addrlist": other_addr})
	else:
		# 添加收货地址
		# 1. 接收数据
		recipient_name = request.POST.get("username")
		recipient_addr = request.POST.get("addr")
		zip_code = request.POST.get("zip_code")
		recipient_phone = request.POST.get("phone")

		#2. 进行校验
		if not all([recipient_name, recipient_addr, zip_code, recipient_phone]):
			return render(request, "users/user_center_site.html", {"errmsg": "参数不必为空"})

		#3. 添加收货地址
		Address.objects.add_one_address(passport_id=passport_id,
										recipient_name=recipient_name,
										recipient_addr=recipient_addr,
										zip_code=zip_code,
										recipient_phone=recipient_phone)

		#4. 返回应答
		return redirect(reverse("user:address"))

@login_required
def order(request):
	'''用户中心－订单号'''
	#查询用户的订单信息
	passport_id = request.session.get("passport_id")

	#获取订单信息
	order_li = OrderInfo.objects.filter(passport_id=passport_id)

	#判断是否存在历史订单
	if not order_li:
		return render(request, "users/user_center_order.html")

	#遍历获取订单的商品信息
	for order in order_li:
		#根据订单id查询订单商品信息
		order_id = order.order_id
		order_books_li = OrderGoods.objects.filter(order_id=order_id)

		#计算商品的小计
		for order_books in order_books_li:
			count = order_books.count
			price = order_books.price
			amount = count * count
			#保存订单中每个商品的小计
			order_books.amount = amount

		#给order对象动态增加一个属性order_goods_li,保存订单中商品的信息
		order.order_books_li = order_books_li

		context = {
			"order_li": order_li,
			"page": "order"
		}
		# print(order_li)
		return render(request, "users/user_center_order.html", context)

@login_required
def del_address(request):
	'''删除用户收货地址'''
	#首先获取到用户的收货地址ｉｄ
	addr_id = request.POST.get("id")

	addr = Address.objects.del_address(addr_id)
	#判断是否删除成功
	if addr:
		#删除成功
		return JsonResponse({"res": 200})
	else:
		#删除错误
		return JsonResponse({"res": 500})

@login_required
def update_address(request):
	'''设置默认收货地址'''
	#首先获取待设置的默认收货地址和用户ｉｄ
	aid = request.POST.get("id")
	passport_id = request.session.get("passport_id")
	addr = Address.objects.update_address(passport_id=passport_id, addr_id=aid)
	if addr:
		return JsonResponse({"res": 200})
	else:
		return JsonResponse({"res": 500})
















