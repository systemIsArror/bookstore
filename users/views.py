#encoding:utf-8
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render,redirect
import re
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection

from books.models import Books
from django.conf import settings
from order.models import OrderInfo, OrderGoods
from .models import Passport,Address
from utils.decorators import login_required
from books.enums import PYTHON
from order.models import OrderInfo
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from users.tasks import send_active_email
from django.core.mail import send_mail

# Create your views here.
def register(request):
	return render(request,'users/register.html')

@transaction.atomic()
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
	passport = Passport.objects.add_one_passport(username=username,password=password,email=email)

	#生产激活的token
	serializer = Serializer(settings.SECRET_KEY, 3600)
	token = serializer.dumps({"confirm": passport.id}) #返回bytes
	token = token.decode()
	# 给用户的邮箱发激活邮件
	# send_active_email.delay(token, username, email)
	subject = "第一份邮件"  # 标题
	message = ""
	sender = settings.EMAIL_FROM  # 发件人
	receiver = [email]  # 收件人列表
	html_message = "<a href='http://192.168.16.60:8000/user/active/%s/'>http://192.168.16.60:8000/user/active/</a>" % token
	send_mail(subject, message, sender, receiver, html_message=html_message)
	return redirect(reverse('user:login'))


def user_login(request):
	return render(request, 'users/login.html')

@csrf_exempt
def login_handle(request):

	'''进行用户登录验证'''
	username = request.POST.get("username")
	password = request.POST.get("password")
	remember = request.POST.get("remember")
	vc = request.POST.get("verifycode")
	if not all([username,password,vc]):
		return JsonResponse({"res": 2})

	if vc.upper() != request.session.get("verifycode"):
		return JsonResponse({"res": 3})

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

	#获取用户的最近浏览信息
	con = get_redis_connection("default")
	key = 'history_%d' % passport_id
	#取出用户最近浏览的5个商品id
	history_li = con.lrange(key, 0, 4)
	
	# books_li = Books.objects.get_books_by_type(PYTHON)
	books_li = []
	for id in history_li:
		books = Books.objects.get_books_by_id(books_id=id)
		books_li.append(books)

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
		order.status = OrderInfo.ORDER_STATUS_CHOICES[order.status-1][1]

		#计算商品的小计
		for order_books in order_books_li:
			count = order_books.count
			price = order_books.price
			amount = count * price
			#保存订单中每个商品的小计
			order_books.amount = amount

		#给order对象动态增加一个属性order_goods_li,保存订单中商品的信息
		order.order_books_li = order_books_li

	context = {
		"order_li": order_li,
		"page": "order"
	}
	print(order_li)
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

#验证码
def verifycode(request):
	#引入绘图模块
	from PIL import Image, ImageDraw, ImageFont
	#引入随机函数数模块
	import random
	#定义变量，用于换面的背景色，宽，高
	bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
	width = 100
	height = 25
	#创建画面对象
	im = Image.new("RGB", (width, height), bgcolor)
	#创建画笔对象
	draw = ImageDraw.Draw(im)
	#调用画笔的point()函数绘制噪点
	for i in range(0, 100):
		xy = (random.randrange(0, width), random.randrange(0, height))
		fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
		draw.point(xy, fill=fill)
	#定义验证码的备选值
	str1 = "ABCD123EFG0703HIGK682720MNOPQ34210RSJOVWSNXZ"
	#随机选取４个值作为验证码
	rand_str = ""
	for i in range(0, 4):
		rand_str += str1[random.randrange(0, len(str1))]
	#构造字体对象
	font = ImageFont.truetype("/usr/share/fonts/truetype/fonts-japanese-gothic.ttf", 15)
	#构造字体颜色
	fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
	#绘制4个字
	draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
	draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
	draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
	draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)

	#释放画笔
	del draw
	#存入session,用于作进一步验证
	request.session["verifycode"] = rand_str
	#内存文件操作
	import io
	buf = io.BytesIO()
	#将图片保存在内存中，看文件类型为png
	im.save(buf, "png")
	#将内存中的图片数据返回给客户端，MIME类型为图片png
	return HttpResponse(buf.getvalue(), "image/png")

def register_active(request, token):
	'''用户账户激活'''
	serializer = Serializer(settings.SECRET_KEY,3600)
	try:
		info = serializer.loads(token)
		passport_id = info["confirm"]
		#进行用户激活
		passport = Passport.objects.get(id=passport_id)
		passport.is_active = True
		passport.save()
		#跳转到登录页
		return redirect(reverse("user:login"))
	except SignatureExpired:
		#链接过期
		return HttpResponse("激活链接已过期")











