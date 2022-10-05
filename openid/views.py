import json
import requests
import jwt
import time
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from openid import models as openid_models
from oauth import models
from user import models as user_models


# Create your views here.

# 注册Oauth服务
def oidc_register_oauth(request):
    host = "http://" + request.get_host()
    headers = {'content-type': "application/json"}
    body = {"app_name": "oidc", "client_type": "confidential",
            "redirect_uri": "http://127.0.0.1:8001/oidc/authorize/callback"}
    res = requests.post(host + "/oauth/register", data=json.dumps(body), headers=headers)
    js_res = json.loads(res.content.decode())
    client_id = js_res.get("client_id")
    client_secret = js_res.get("client_secret")
    oauth_obj = openid_models.ClientInformation(app_name="oidc", client_id=client_id, client_secret=client_secret)
    oauth_obj.save()
    return JsonResponse({"client_id": client_id, "client_secret": client_secret})


def oidc_authorize_callback(request):
    if request.method == "GET":
        code = request.GET.get("code")
        state = request.GET.get("state")
        return JsonResponse({"code": code, "state": state})


# 获取Authorization Code
def oidc_authorize(request):
    if request.method == "GET":
        host = "http://" + request.get_host()
        scope = request.GET.get("scope")
        response_type = request.GET.get("response_type")
        client_id = request.GET.get("client_id")
        redirect_uri = request.GET.get("redirect_uri")
        state = request.GET.get("state")

        # 获取Authorization Code
        url = "%s/oauth/authorize?response_type=%s&scope=%s&client_id=%s&redirect_uri=%s&state=%s" % \
              (host, response_type, scope, client_id, host + "/oidc/authorize/callback", state)
        return redirect(url)
        # res = requests.get(url)
        # js_res = json.loads(res.content.decode())
        # code = js_res.get("code")
        # return redirect(redirect_uri + ("?code=%s&state=%s" % (code, state)))


def generate_id_token(host, sub, aud, exp, iat, auth_time, client_secret):
    data = {
        "iss": host,
        "sub": sub,
        "aud": aud,
        "exp": exp,
        "iat": iat,
        "auth_time": auth_time
    }
    jwt_encode = jwt.encode(data, client_secret, algorithm='HS256')
    return jwt_encode


# 获取token
def oidc_token(request):
    if request.method == "POST":
        req = json.loads(request.body)
        client_id = req.get("client_id")
        client_secret = req.get("client_secret")
        grant_type = req.get("grant_type")
        code = req.get("code")
        redirect_uri = req.get("redirect_uri")
        username = models.CodeToUsername.objects.filter(code=code).first().username
        auth_time = models.CodeToUsername.objects.filter(code=code).first().auth_time
        host = "http://" + request.get_host()
        headers = {'content-type': "application/json"}
        body = {"client_id": client_id, "client_secret": client_secret, "grant_type": grant_type, "code": code,
                "redirect_uri": redirect_uri}
        res = requests.post(host + "/oauth/token", data=json.dumps(body), headers=headers)
        js_res = json.loads(res.content.decode())
        access_token = js_res.get("access_token")
        refresh_token = js_res.get("refresh_token")
        token_type = js_res.get("token_type")
        expires_in = js_res.get("expires_in")
        cur_time = timezone.now()
        time_tp = cur_time.timetuple()
        exp = time.mktime(time_tp) + expires_in
        id_token = generate_id_token(host, username, client_id, exp, exp - expires_in, auth_time, client_secret)
        res.headers = {"Cache-Control": "no-store", "Pragma": "no-cache"}
        return JsonResponse({"access_token": access_token, "token_type": token_type, "refresh_token": refresh_token,
                             "expires_in": expires_in, "id_token": id_token})


def oidc_user_info(request):
    if request.method == "GET":
        req = str(request.META.get("HTTP_AUTHORIZATION"))
        token = req.split()
        token = token[1]
        token_obj = models.TokenToUsername.objects.filter(token=token).first()
        if token_obj:
            host = "http://" + request.get_host()
            headers = {'content-type': "application/json"}
            body = {"access_token": token}
            res = requests.post(host + "/oauth/verify", data=json.dumps(body), headers=headers)
            js_res = json.loads(res.content.decode())
            success = js_res.get("success")
            if success:
                username = token_obj.username
                user_obj = user_models.User.objects.filter(username=username).first()
                email = user_obj.email
                intro = user_obj.intro
                return JsonResponse({"sub": username, "email": email, "intro": intro})
            else:
                return JsonResponse({"success": False, "msg": "token校验失败"})
        else:
            return JsonResponse({"success": False, "msg": "token校验失败"})
