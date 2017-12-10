#encoding:utf-8
from __future__ import unicode_literals

from django.db import models
from db.basemodel import BaseModel
from hashlib import sha1

#hash加密
def get_hash(str):
	sh = sha1()
	sh.update(str.encode("utf-8"))
	return sh.hexdigest()

class PassportManager(models.Manager):

	def add_one_passport(self,username,password,email):
		'''
		添加账号信息
		'''
		return self.create(username=username, password=get_hash(password), email=email)

	def get_one_passport(self,username,password):
		'''根据用户名和密码查找账户信息'''
		try:
			return self.get(username=username, password=get_hash(password))
		except:
			#账户不存在
			return None

	def check_passport(self,username):
		try:
			passport = self.get(username=username)
		except self.model.DoesNotExist:
			passport = None
		return passport

class Passport(BaseModel):
	'''
	数据库抽象类
	'''
	username = models.CharField(max_length=20,verbose_name='用户名称')
	password = models.CharField(max_length=40,verbose_name='密码')
	email = models.EmailField(verbose_name='用户邮箱')
	is_active = models.BooleanField(default=False,verbose_name='激活状态')

	#用户表的管理器
	objects = PassportManager()

	class Meta:
		db_table = 's_user_account'


class AddressManager(models.Manager):
	'''地址模型管理器类'''
	def get_default_address(self,passport_id):
		'''查询指定用户的默认收货地址'''
		try:
			addr = self.get(passport_id=passport_id, is_default=True, is_delete=False)
		except self.model.DoesNotExist:
			#没有默认收货地址
			addr = None
		return addr

	def add_one_address(self,passport_id, recipient_name, recipient_addr, zip_code, recipient_phone):
		'''添加收货地址'''
		#判断用户是否有默认收货地址
		addr = self.get_default_address(passport_id=passport_id)

		if addr:
			#存在默认地址
			is_default = False
		else:
			#不存在默认地址
			is_default = True
		#添加一个地址
		addr = self.create(passport_id=passport_id,
							recipient_name=recipient_name,
							recipient_addr=recipient_addr,
							zip_code=zip_code,
							recipient_phone=recipient_phone,
							is_default=is_default)
		return addr

	def get_other_address(self,passport_id):
		'''查询指定用户的非默认收货地址'''
		try:
			addr = self.filter(passport_id=passport_id, is_default=False, is_delete=False)
		except self.model.DoesNotExist:
			#没有默认收货地址
			addr = None
		return addr

	def del_address(self,addr_id):
		'''删除用户收货地址'''
		try:
			#get如果获取到多条信息会报错
			addr = self.get(id=addr_id)
			if addr:
				addr.is_delete= True
				addr.save()
		except self.model.DoesNotExist:
			#收货地址错误
			addr = None
		return addr

	def update_address(self,passport_id,addr_id):
		'''更改用户默认收货地址'''
		try:
			#首先判断收地地址是否在数据库中存在，如果存在才修改默认收货地址
			addr = self.get(id=addr_id)
			if addr:
				self.filter(passport_id=passport_id).update(is_default=False)
				addr.is_default = True
				addr.save()
		except self.model.DoesNotExist:
			#收货地址错误
			addr = None
		return addr

class Address(BaseModel):
	'''地址模型类'''
	recipient_name = models.CharField(max_length=20, verbose_name='收件人')
	recipient_addr = models.CharField(max_length=256, verbose_name='收件地址')
	zip_code = models.CharField(max_length=6, verbose_name='邮政编码')
	recipient_phone = models.CharField(max_length=11, verbose_name='联系电话')
	is_default = models.BooleanField(default=False, verbose_name='是否默认地址')
	passport = models.ForeignKey('Passport', verbose_name='账户')

	objects = AddressManager()

	class Meta:
		db_table = 's_user_address'





