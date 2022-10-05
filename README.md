# bangumoe

## 每日学习日志

[传送门](https://github.com/patricklai46/bingyannote)

## 阶段一

> 实现最基本的用户注册登录和修改信息的API

- 使用 `MySQL` 存储用户数据
- 利用 `django` 作为后端框架

### 注册 POST /register

```json
{
    "username": "xxx",
    "password": "xxx",
    "email": "xxx",
    "intro": "xxx"
}
```

返回：

````json
{
    "success": True,
    "code": "register_success",
    "msg": "注册成功"
}
````

### 登录 POST /login

```json
{
    "username": "xxx",
    "password": "xxx"
}
```

返回：

````json
{
    "success": True,
    "code": "login_success",
    "msg": "登录成功"
}
````

### 修改信息 POST /edit_profile

```json
{
    "user_id": xxx,
    "username": "xxx",
    "password": "xxx",
    "email": "xxx",
    "intro": "xxx"
}
```

返回：

````json
{
    "success": True,
    "code": "edit_profile_success",
    "msg": "修改信息成功"
}
````

## 阶段二&三

> 实现使用 Authorization Code模式的OAuth2.0服务

### 客户端注册 POST /oauth/register

```json
{
    "app_name": "xxx",
    "client_type": "confidential",
    "redirect_url": "https://auth.kkkstra.cn/callback"
}
```

> **注册客户端信息：**
>
> `app_name`: 应用名称
>
> `client_type`: 有 `confidential` 和 `public` 两种
>
> `redtrect_url`: 重定向url

返回：

```json
{
    "success": true,
    "client_id": "xxx",
    "client_secret": "xxx",
    "msg": "注册成功"
}
```

### 获取Authorization code GET /oauth/authorize

```json
{
    "response_type": "code",
    "client_id": "xxx",
    "redirect_url": "https://auth.kkkstra.cn/callback",
    "scope": "read",
    "state": "xxx"
}
```

> `client_ud`: 应用id
>
> `redtrect_url`: 重定向url
>
> `scope`: 授权权限
>
> `state`: [参考博客](https://www.cnblogs.com/blowing00/p/14872312.html)

返回：

````http
HTTP/1.1 302 Found
     Location: https://auth.kkkstra.cn/callback?code=AuthorizationCode&state=test
````

`error` 参考[官方文档](https://www.rfc-editor.org/rfc/rfc6749#section-4.1.2)

### 获取Access token POST /oauth/token

```json
{
    "grant_type": "authorization_code",
    "client_id": "ZJSNaNGu0C9Y1CJxarFjEfWDdgraIKX6",
    "client_secret": "mFh5ZkKp2cDFqT8COy9dHjMhM9bQkv0hNURLl2dZIsa9yac_4VtwNEwpIhhoU4y-Ah5t7uma8BxcG8walIMzHg",
    "code": "vSRe0crW8O6O5cuI74GUvoV9SyWo6I3k",
    "redirect_url": "https://auth.kkkstra.cn/callback"
}
```

> `grant_type`: 授权方式
>
> `client_ud`: 应用id
>
> `client_secret`: 应用密钥
>
> `code`: Authorization code
>
> `redtrect_url`: 重定向url

返回：

```json
{
    "access_token": "xxx",
    "token_type": "bearer",
    "expires_in": 60,
    "refresh_token": "xxx",
    "scope": "read"
}
```

`error` 参考[官方文档](https://www.rfc-editor.org/rfc/rfc6749#section-5.2)

### 使用Refresh Token刷新Access Token

```json
{
    "grant_type": "refresh_token",
    "refresh_token": "xxx",
    "scope": "xxx"
}
```

> `grant_type`: 授权方式
>
> `refresh_token`: Refresh Token
>
> `scope`: 可选项

返回：

```json
{
    "access_token": "xxx",
    "token_type": "bearer",
    "expires_in": 60,
    "refresh_token": "xxx",
    "scope": "read"
}
```

`error` 参考[官方文档](https://www.rfc-editor.org/rfc/rfc6749#section-5.2)

### 校验Access Token POST /oauth/verify

```json
{
    "access_token": "xxx"
}
```

返回：

```json
{
    "success": true,
    "msg": "Access token校验成功"
}
```

# 阶段四

### 在OAuth中为OIDC服务注册应用信息 GET /oidc/register

返回：

```json
{
    "client_id": "xxx",
    "client_secret": "xxx"
}
```

### 获取code GET /oidc/authorize

```json
{
    "response_type": "code",
    "client_id": "xxx",
    "scope": "openid email profile",
    "redirect_uri": "http://127.0.0.1:8001/oidc/authorize/callback",
    "state": "xxx"
}
```

返回：

```http
  HTTP/1.1 302 Found
  Location: https://client.example.org/cb?
    code=SplxlOBeZQQYbYS6WxSbIA
    &state=af0ifjsldkj
```

### 获取Access Token POST /oidc/token

```json
{
    "access_token": "xxx",
    "token_type": "bearer",
    "expires_in": 60,
    "refresh_token": "xxx",
    "scope": "read"
}
```

返回：

```json
  HTTP/1.1 200 OK
  Content-Type: application/json
  Cache-Control: no-store
  Pragma: no-cache

  {
   "access_token": "SlAV32hkKG",
   "token_type": "Bearer",
   "refresh_token": "8xLOxBtZp8",
   "expires_in": 3600,
   "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjFlOWdkazcifQ.ewogImlzc
     yI6ICJodHRwOi8vc2VydmVyLmV4YW1wbGUuY29tIiwKICJzdWIiOiAiMjQ4Mjg5
     NzYxMDAxIiwKICJhdWQiOiAiczZCaGRSa3F0MyIsCiAibm9uY2UiOiAibi0wUzZ
     fV3pBMk1qIiwKICJleHAiOiAxMzExMjgxOTcwLAogImlhdCI6IDEzMTEyODA5Nz
     AKfQ.ggW8hZ1EuVLuxNuuIJKX_V8a_OMXzR0EHR9R6jgdqrOOF4daGU96Sr_P6q
     Jp6IcmD3HP99Obi1PRs-cwh3LO-p146waJ8IhehcwL7F09JdijmBqkvPeB2T9CJ
     NqeGpe-gccMg4vfKjkM8FcGvnzZUN4_KSP0aAp1tOJ1zZwgjxqGByKHiOtX7Tpd
     QyHE5lcMiKPXfEIQILVq0pc_E2DzL7emopWoaoZTF_m0_N0YzFC6g6EJbOEoRoS
     K5hoDalrcvRYLSrQAZZKflyuVCyixEoV9GfNQC3_osjzw2PAithfubEEBLuVVk4
     XUVrWOLrLl0nx7RkKU8NXNHq-rvKMzqg"
  }
```

### 获取UserIndo EndPoint GET /oidc/user_info

```http
  GET /userinfo HTTP/1.1
  Host: 127.0.0.1:8001
  Authorization: Bearer SlAV32hkKG
```

返回：

```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "sub": "xxx",
    "email": "xxx",
    "intro": "xxx"
}
```

