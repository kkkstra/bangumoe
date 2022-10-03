from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from oauth import models
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
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


# 生成授权码
def generate_authorization_code():
    alphabet = string.ascii_letters + string.digits
    while True:
        code = ''.join(secrets.choice(alphabet) for i in range(32))
        if (any(c.islower() for c in code)
                and any(c.isupper() for c in code)
                and any(c.isupper() for c in code)):
            break
    return code


# 生成access token
def generate_token():
    return secrets.token_urlsafe(nbytes=64)


# 注册应用信息
def register_application(request):
    if request.method == "POST":
        req = json.loads(request.body)
        app_name = req.get("app_name")
        client_id = generate_client_id()
        client_type = 0
        client_secret = ""
        if req.get("client_type") == "confidential":
            client_type = 1
            client_secret = generate_client_secret()
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


# 获取authorization code
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
                    code_obj = models.AuthorizationCode.objects.filter(client_id=client_id).first()
                    if code_obj:
                        models.AuthorizationCode.objects.filter(client_id=client_id).update(code=code,time=timezone.now())
                    else:
                        code_obj = models.AuthorizationCode(client_id=client_id, code=code, scope=scope,time=timezone.now())
                        code_obj.save()
                    url = "%s?code=%s&state=%s" % (redirect_url, code, state)
                    return redirect(url)
                else:
                    return JsonResponse({"success": False, "msg": "重定向URL错误"})
            else:
                return JsonResponse({"success": False, "msg": "应用未注册"})


# 获取access token
def token(request):
    if request.method == "POST":
        req = json.loads(request.body)
        client_id = req.get("client_id")
        client_secret = req.get("client_secret")
        grant_type = req.get("grant_type")
        code = req.get("code")
        redirect_url = req.get("redirect_url")
        # 验证身份
        app_obj = models.Application.objects.filter(client_id=client_id).first()
        if app_obj:
            if ((app_obj.client_type == 0) or (app_obj.client_type and client_secret == app_obj.client_secret)) and (
                    redirect_url == app_obj.redirect_url):
                if grant_type == "authorization_code":
                    # 校验身份码
                    code_obj = models.AuthorizationCode.objects.filter(client_id=client_id).first()
                    if code_obj and code == code_obj.code:
                        duration = timedelta.total_seconds(timezone.now() - code_obj.time)
                        if duration > 600:
                            return JsonResponse({"success": False, "msg": "Authorization code已过期"})
                        else:
                            # 生成token
                            access_token = generate_token()
                            refresh_token = generate_token()
                            scope = code_obj.scope
                            token_obj = models.AccessToken(access_token=access_token, refresh_token=refresh_token,
                                                           scope=scope)
                            token_obj.save()
                            return JsonResponse({"access_token": access_token, "token_type": "bearer",
                                                 "expires_in": token_obj.expires_in, "refresh_token": refresh_token,
                                                 "scope": scope})
                    else:
                        return JsonResponse({"success": False, "msg": "身份验证失败"})
            else:
                return JsonResponse({"success": False, "msg": "身份验证失败"})
        else:
            return JsonResponse({"success": False, "msg": "身份验证失败"})


# 校验token
def verify(request):
    if request.method == "POST":
        req = json.loads(request.body)
        access_token = req.get("access_token")
        token_obj = models.AccessToken.objects.filter(access_token=access_token).first()
        if token_obj:
            duration = timedelta.total_seconds(timezone.now() - token_obj.time)
            if duration > token_obj.expires_in:
                return JsonResponse({"success": False, "msg": "Access token已过期"})
            else:
                return JsonResponse({"success": True, "msg": "Access token校验成功"})
        else:
            return JsonResponse({"success": False, "msg": "Access token不存在"})
