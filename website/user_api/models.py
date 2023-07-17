from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.

class AppUserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		user = self.model(email=email)
		user.set_password(password)
		user.save()
		return user
	def create_superuser(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.create_user(email, password)
		user.is_superuser = True
		user.save()
		return user

# https://testdriven.io/blog/django-custom-user-model/
class AppUser(AbstractBaseUser, PermissionsMixin):
	user_id = models.AutoField(primary_key=True)
	email = models.EmailField(_("email address"), unique=True)
	username = models.CharField(max_length=150, null=True)
	# email = models.EmailField(max_length=50, unique=True)
	# is_staff = models.BooleanField(default=False)
	# is_active = models.BooleanField(default=True)
	user_type = models.IntegerField(default=1)
	date_joined = models.DateTimeField(default=timezone.now)

	 
	USERNAME_FIELD = "email"
	# REQUIRED_FIELDS = ['username']
	REQUIRED_FIELDS = []
	objects = AppUserManager()
	
	class Meta:
		managed = True
		db_table = 'user_data\".\"user'
	
	def __str__(self):
		# return self.username
		return self.email
