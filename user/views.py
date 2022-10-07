import time, requests, bcrypt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from user import models
import json


# Create your views here.

# 加密密码
def encrypt_passwd(passwd):
    passwd = passwd.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed


# 校验密码
def checkpwd(passwd, hashed):
    passwd = passwd.encode()
    hashed = hashed.encode()
    return bcrypt.checkpw(passwd, hashed)


# 注册
def user_register(request):
    if request.method == "POST":
        req = json.loads(request.body)
        if req.get("username") and req.get("password"):
            username = req.get("username")
            passwd = req.get("password")
            password = encrypt_passwd(passwd)  # 加密密码
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
                user_obj = models.User(username=username, password=password.decode(), email=email, intro=intro)
                user_obj.save()
                return JsonResponse(
                    {"success": True, "code": "register_success", "msg": "注册成功", "uid": user_obj.id})
        else:
            return JsonResponse({"success": False, "code": "username_password_empty", "msg": "用户名或密码不能为空"})


# 登录
def user_login(request):
    if request.method == "POST":
        req = json.loads(request.body)
        if req.get("username") and req.get("password"):
            username = req.get("username")
            password = req.get("password")
            user_obj = models.User.objects.filter(username=username).first()
            if user_obj:
                if checkpwd(password, user_obj.password):
                    return JsonResponse({"success": True, "code": "login_success", "msg": "登录成功"})
                else:
                    return JsonResponse({"success": False, "code": "password_mistaken", "msg": "密码错误"})
            else:
                return JsonResponse({"success": False, "code": "user_not_exist", "msg": "用户不存在"})
        else:
            return JsonResponse({"success": False, "code": "username_password_empty", "msg": "用户名或密码不能为空"})
    # else:
    #     return render(request, 'user/login.html', locals())


# 修改信息
def user_edit_profile(request):
    if request.method == "POST":
        req = json.loads(request.body)
        user_id = req.get("user_id")
        user_obj = models.User.objects.filter(id=user_id).first()
        # 身份验证
        username = req.get("username")
        password = req.get("password")
        if user_obj:
            if username == user_obj.username and checkpwd(password, user_obj.password):
                if req.get("new_username"):
                    new_username = req.get("new_username")
                    if len(models.User.objects.filter(
                            username=new_username)) != 0 and new_username != user_obj.username:
                        return JsonResponse({"success": False, "code": "username_exist", "msg": "用户名已经存在"})
                    elif len(new_username) == 0:
                        return JsonResponse({"success": False, "code": "username_empty", "msg": "用户名不能为空"})
                    else:
                        models.User.objects.filter(id=user_id).update(username=new_username)
                if req.get("new_password"):
                    passwd = req.get("new_password")
                    if len(passwd):
                        new_password = encrypt_passwd(passwd)  # 加密密码
                        models.User.objects.filter(id=user_id).update(password=new_password.decode())
                    else:
                        return JsonResponse({"success": False, "code": "password_empty", "msg": "密码不能为空"})
                if req.get("email"):
                    models.User.objects.filter(id=user_id).update(email=req.get("email"))
                if req.get("intro"):
                    models.User.objects.filter(id=user_id).update(intro=req.get("intro"))
                return JsonResponse({"success": True, "code": "edit_profile_success", "msg": "修改用户信息成功"})
            else:
                return JsonResponse({"success": False, "code": "password_mistaken", "msg": "密码错误"})
        else:
            return JsonResponse({"success": False, "code": "user_not_exist", "msg": "用户不存在"})


def user_oidc(request):
    if request.method == "POST":
        response_type = request.GET.get("response_type")
        client_id = request.GET.get("client_id")
        redirect_uri = request.GET.get("redirect_uri")
        scope = request.GET.get("scope")
        state = request.GET.get("state")
        host = "http://" + request.get_host()
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 进行登录
        res = requests.post(host + "/user/login/", json={"username": username, "password": password})
        success = json.loads(res.content.decode()).get("success")
        cur_time = timezone.now()
        time_tp = cur_time.timetuple()
        auth_time = time.mktime(time_tp)
        if success:
            url = "%s/oauth/authorize/callback?response_type=%s&scope=%s&client_id=%s&redirect_uri=%s&state=%s&username=%s&auth_time=%s" \
                  % (host, response_type, scope, client_id, redirect_uri, state, username,
                     str(auth_time))
            return redirect(url)
        else:
            return JsonResponse({"success": False})
    else:
        response_type = request.GET.get("response_type")
        client_id = request.GET.get("client_id")
        redirect_uri = request.GET.get("redirect_uri")
        scope = request.GET.get("scope")
        state = request.GET.get("state")
        return render(request, "user/auth.html", locals())
