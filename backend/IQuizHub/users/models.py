from django.db import models
from django.contrib.auth.models import AbstractUser


# from questions.models import Question


class User(AbstractUser):
    """用户模型类"""
    # 增加mobile字段
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号', null=True)
    avatar = models.ImageField(verbose_name='头像', blank=True, null=True, upload_to='avatar')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
    introduction = models.TextField(verbose_name='个人简介', blank=True, null=True)
    historys = models.ManyToManyField('History', verbose_name='历史记录', related_name='history')

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


class Comment(models.Model):
    comment = models.TextField(verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='作者')
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, verbose_name='问题')

    class Meta:
        db_table = 'comments'
        verbose_name = '评论表'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.comment


class History(models.Model):
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, verbose_name='问题')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    correct = models.BooleanField(verbose_name='是否正确')
    # users = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')


    class Meta:
        db_table = 'history'
        verbose_name = '历史记录表'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
