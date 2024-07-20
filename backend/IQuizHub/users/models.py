from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """用户模型类"""
    # 增加mobile字段
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号', null=True)
    # mobile = models.CharField(max_length=11, verbose_name='手机号', null=True)
    avatar = models.ImageField(verbose_name='头像', blank=True, null=True, upload_to='avatar')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
    # introduction = models.CharField(max_length=100, verbose_name='个人简介', blank=True, null=True)
    introduction = models.TextField(verbose_name='个人简介', blank=True, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用户表'


class Captcha(models.Model):
    """验证码模型类"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    captcha = models.CharField(max_length=4, verbose_name='验证码')
    # user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', null=True)

    class Meta:
        db_table = 'captcha'
        verbose_name = '验证码表'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.mobile
