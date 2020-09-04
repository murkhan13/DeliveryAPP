from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
# from blissedmath.utils import unique_otp_generator
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# from catalog.models import Restaurant

import random
import os
import requests


class UserManager(BaseUserManager):
    def create_user(self, phone, is_staff=False, is_active=True, is_admin=False):
        if not phone :
            raise ValueError('Пользователь должен иметь номер телефона')
        """if not password:
            raise ValueError('Пользователь должен иметь пароль')

        password=None, """

        user_obj = self.model(
            phone=phone
        )
        # user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None, is_admin=False, is_staff=True, is_active=True):

        user_obj = self.model(
            phone=phone
        )
        user_obj.set_password(password)
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.staff = is_staff
        user = user_obj
        user.save(using=self._db)
        return user
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, phone, password, is_active=True, is_staff=True, is_admin=True):

        if not phone :
            raise ValueError('Пользователь должен иметь номер телефона')
        if not password:
            raise ValueError('Пользователь должен иметь пароль')

        user_obj = self.model(
            phone=phone
        )
        user_obj.set_password(password)
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.staff = is_staff
        user = user_obj
        user.save(using=self._db)
        return user


        # user = self.create_user(
        #     phone,
        #     password=password,
        #     is_staff=True,
        #     is_admin=True
        # )
        # user.save(using=self._db)
        # return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model class that represents a user, with some rules that set in UserManager class

    Args:
        AbstractBaseUser ([class]): [class from django]
        PermissionsMixin ([class]): [class mixin from django]

    Returns:
        [type]: [description]
    """
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,30}$',#regex=r'^\+?1?\d{9,15}$'regex=r'^\+?1?\d{11,25}$',
                                message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators = [phone_regex], max_length=25, unique=True)
    name        = models.CharField(max_length=20, blank=True, null=True)
    first_login = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.name:
            return self.name
        else:
            return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    class Meta:
        verbose_name_plural = "Пользователи"


class PhoneOTP(models.Model):
    """
    Model class that represents a otp that generate and send to the user while authorizing

    Args:
        models ([class]): [model class from django]

    Returns:
        [string]: [information of object to django admin panel]
    """
    phone_regex = RegexValidator(regex=r'^\+?1?\d{11,25}$',
                                message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone               = models.CharField(validators = [phone_regex], max_length=25, unique=True)
    otp                 = models.CharField(max_length = 9, blank = True, null = True)
    count               = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    validated           = models.BooleanField(default = False, help_text='If it is true, that means user have validate otp correctly in second API')
    favoriteRestaurants = models

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)