#encoding:utf-8
from django.http import JsonResponse
from django.shortcuts import render,redirect
import re
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
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
	if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
		return render(request,'users/register.html',{'errormsg':'邮箱格式不对！'})
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

















