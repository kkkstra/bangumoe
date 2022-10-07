import secrets
import string
import time, requests, bcrypt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from user import models
from django.core.mail import send_mail
from oidc.settings import EMAIL_FROM
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


# 生成验证码
def generate_verify_code():
    alphabet = string.ascii_letters + string.digits
    while True:
        verify_code = ''.join(secrets.choice(alphabet) for i in range(6))
        if (any(c.islower() for c in verify_code)
                and any(c.isupper() for c in verify_code)
                and any(c.isupper() for c in verify_code)):
            break
    return verify_code


def send_verify_email(email, code):
    email_title = 'bangumoe - 注册激活链接'
    email_body = '您的激活验证码为%s，请点击下方的链接激活你的账号：http://127.0.0.1:8001/user/activate/' % code
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 注释 ①


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
            user_obj = models.User.objects.filter(username=username).first()
            if user_obj:
                if user_obj.activated:
                    return JsonResponse({"success": False, "code": "user_exist", "msg": "用户已存在"})
                else:
                    code = generate_verify_code()
                    send_verify_email(email, code)
                    models.User.objects.filter(username=username).update(password=password.decode(), email=email,
                                                                         intro=intro,
                                                                         code=code)
                    return JsonResponse(
                        {"success": True, "code": "register_success", "msg": "注册成功，请使用验证码激活账号",
                         "uid": user_obj.id})
            else:
                code = generate_verify_code()
                # 发送注册邮件
                send_verify_email(email, code)
                user_obj = models.User(username=username, password=password.decode(), email=email, intro=intro,
                                       code=code)
                user_obj.save()
                return JsonResponse(
                    {"success": True, "code": "register_success", "msg": "注册成功，请使用验证码激活账号",
                     "uid": user_obj.id})
        else:
            return JsonResponse({"success": False, "code": "username_password_empty", "msg": "用户名或密码不能为空"})


def user_activate(request):
    if request.method == "POST":
        req = json.loads(request.body)
        username = req.get("username")
        password = req.get("password")
        code = req.get("code")
        user_obj = models.User.objects.filter(username=username).first()
        if user_obj:
            if checkpwd(password, user_obj.password):
                if user_obj.activated:
                    return JsonResponse({"success": False, "code": "already_activated", "msg": "用户已激活"})
                else:
                    if code == user_obj.code:
                        models.User.objects.filter(username=username).update(activated=True)
                        return JsonResponse({"success": True, "code": "successfully_activated", "msg": "账号激活成功"})
                    else:
                        return JsonResponse({"success": False, "code": "code_wrong", "msg": "验证码错误"})
            else:
                return JsonResponse({"success": False, "code": "password_mistaken", "msg": "密码错误"})
        else:
            return JsonResponse({"success": False, "code": "user_not_exist", "msg": "用户不存在"})


# 登录
def user_login(request):
    if request.method == "POST":
        req = json.loads(request.body)
        if req.get("username") and req.get("password"):
            username = req.get("username")
            password = req.get("password")
            user_obj = models.User.objects.filter(username=username).first()
            if user_obj and user_obj.activated:
                if checkpwd(password, user_obj.password):
                    return JsonResponse({"success": True, "code": "login_success", "msg": "登录成功"})
                else:
                    return JsonResponse({"success": False, "code": "password_mistaken", "msg": "密码错误"})
            else:
                return JsonResponse({"success": False, "code": "user_not_exist", "msg": "用户不存在或未激活"})
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
        if user_obj and user_obj.activated:
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
                    email = req.get("email")
                    models.User.objects.filter(id=user_id).update(email=email)
                if req.get("intro"):
                    models.User.objects.filter(id=user_id).update(intro=req.get("intro"))
                return JsonResponse({"success": True, "code": "edit_profile_success", "msg": "修改用户信息成功"})
            else:
                return JsonResponse({"success": False, "code": "password_mistaken", "msg": "密码错误"})
        else:
            return JsonResponse({"success": False, "code": "user_not_exist", "msg": "用户不存在或未激活"})


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
