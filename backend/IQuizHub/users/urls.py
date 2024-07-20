"""
URL configuration for IQuizHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView

from users.views import LoginView, RigisterView, UserView, CaptchaView

urlpatterns = [
    path('login/', LoginView.as_view(), name='登录'),
    path("register/", RigisterView.as_view(), name='注册'),
    path("capatcha/", CaptchaView.as_view(), name='验证码'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("token/verify/", TokenVerifyView.as_view(), name='token_verify'),
    path("users/<int:pk>/", UserView.as_view({'get': 'retrieve'}), name='用户详情'),
    path("<int:pk>/avatar/upload/", UserView.as_view({'post': 'avatar_upload'}), name='头像上传'),
    path("<int:pk>/introduction/", UserView.as_view({'post': 'upload_introduction'}), name='个人简介'),
]