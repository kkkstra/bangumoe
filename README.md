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