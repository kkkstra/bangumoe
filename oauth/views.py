from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from oauth import models
from django.shortcuts import redirect
import json, secrets, string


# Create your views here.

def generate_client_id():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(32))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isupper() for c in password)):
            break
    return password


def generate_client_secret():
    client_key = secrets.token_urlsafe(nbytes=64)
    return client_key


def generate_authorization_code():
    alphabet = string.ascii_letters + string.digits
    while True:
        code = ''.join(secrets.choice(alphabet) for i in range(32))
        if (any(c.islower() for c in code)
                and any(c.isupper() for c in code)
                and any(c.isupper() for c in code)):
            break
    return code


# 注册应用信息
def register_application(request):
    if request.method == "POST":
        req = json.loads(request.body)
        app_name = req.get("app_name")
        client_id = req.get("client_id")
        if client_id == "":
            client_id = generate_client_id()
        client_secret = req.get("client_secret")
        if client_secret == "":
            client_secret = generate_client_secret()
        client_type = 0
        if req.get("client_type") == "confidential":
            client_type = 1
        redirect_url = req.get("redirect_url")
        if app_name and client_id and ((client_type and client_secret) or client_type == 0) and redirect_url:
            app_obj = models.Application.objects.filter(app_name=app_name).first()
            if app_obj:
                return JsonResponse({"success": False, "msg": "应用已注册"})
            else:
                user_obj = models.Application(app_name=app_name, client_id=client_id, client_secret=client_secret,
                                              client_type=client_type, redirect_url=redirect_url)
                user_obj.save()
                return JsonResponse({"success": True, "client_id": client_id, "client_secret": client_secret,
                                     "msg": "注册成功"})
        else:
            return JsonResponse({"success": False, "msg": "不能有字段为空"})


# Authorization grant
def auth(request):
    if request.method == "GET":
        response_type = request.GET.get("response_type")
        client_id = request.GET.get("client_id")
        redirect_url = request.GET.get("redirect_url")
        scope = request.GET.get("scope")
        state = request.GET.get("state")
        # Authorization code模式
        if response_type == "code":
            # 验证身份
            app_obj = models.Application.objects.filter(client_id=client_id).first()
            if app_obj:
                if redirect_url == app_obj.redirect_url:
                    # 生成AuthorizationCode
                    code = generate_authorization_code()
                    code_obj = models.AuthorizationCode(client_id=client_id, code=code, scope=scope)
                    code_obj.save()
                    url = "%s?code=%s&state=%s" % (redirect_url, code, state)
                    return redirect(url)
                else:
                    return JsonResponse({"success": False, "msg": "重定向URL错误"})
            else:
                return JsonResponse({"success": False, "msg": "应用未注册"})


# Access token
def token(request):
    if request.method == "GET":
        pass
