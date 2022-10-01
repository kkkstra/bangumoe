"""oidc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path

import users
from users import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),  # 主页
    path('register/', views.register),          # 注册功能
    path('login/', views.login),           # 登陆功能
    path('userlist/', views.userlist),     # 展示用户列表
    path('edit_user/', views.edit_user),   # 管理用户信息
    path('delete_user/', views.delete_user),   # 删除用户
]
