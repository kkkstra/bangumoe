from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from user import models
import json


# Create your views here.

# 注册
def register(request):
    if request.method == "POST":
        req = json.loads(request.body)
        if req.get("username") and req.get("password"):
            username = req.get("username")
            password = req.get("password")
            if req.get("email"):
                email = req.get("email")
            else:
                email = ""
            if req.get("intro"):
                intro = req.get("intro")
            else:
                intro = "这个人很懒，什么都没有留下。"
            user_obj = models.User.objects.filter(username=username)
            if len(user_obj) != 0:
                return JsonResponse({"success": False, "code": "user_exist", "msg": "用户已存在"})
            else:
                user_obj = models.User(username=username, password=password, email=email, intro=intro)
                user_obj.save()
                return JsonResponse({"success": True, "code": "register_success", "msg": "注册成功"})
        else:
            return JsonResponse({"success": False, "code": "username_password_empty", "msg": "用户名或密码不能为空"})


# 登录
def login(request):
    if request.method == "POST":
        req = json.loads(request.body)
        if req.get("username") and req.get("password"):
            username = req.get("username")
            password = req.get("password")
            user_obj = models.User.objects.filter(username=username).first()
            if user_obj:
                if password == user_obj.password:
                    return JsonResponse({"success": True, "code": "login_success", "msg": "登录成功"})
                else:
                    return JsonResponse({"success": False, "code": "password_mistaken", "msg": "密码错误"})
            else:
                return JsonResponse({"success": False, "code": "user_not_exist", "msg": "用户不存在"})
        else:
            return JsonResponse({"success": False, "code": "username_password_empty", "msg": "用户名或密码不能为空"})


# 修改信息
def edit_profile(request):
    if request.method == "POST":
        req = json.loads(request.body)
        user_id = req.get("user_id")
        user_obj = models.User.objects.filter(id=user_id).first()
        if user_obj:
            if req.get("username"):
                username = req.get("username")
                if len(models.User.objects.filter(username=username)) != 0 and username != user_obj.username:
                    return JsonResponse({"success": False, "code": "username_exist", "msg": "用户名已经存在"})
                elif len(username) == 0:
                    return JsonResponse({"success": False, "code": "username_empty", "msg": "用户名不能为空"})
                else:
                    models.User.objects.filter(id=user_id).update(username=username)
            if req.get("password"):
                password = req.get("password")
                if len(password):
                    models.User.objects.filter(id=user_id).update(username=req.get("password"))
                else:
                    return JsonResponse({"success": False, "code": "password_empty", "msg": "密码不能为空"})
            if req.get("email"):
                models.User.objects.filter(id=user_id).update(email=req.get("email"))
            if req.get("intro"):
                models.User.objects.filter(id=user_id).update(intro=req.get("intro"))
            return JsonResponse({"success": True, "code": "edit_profile_success", "msg": "修改用户信息成功"})
        else:
            return JsonResponse({"success": False, "code": "user_not_exist", "msg": "用户不存在"})
