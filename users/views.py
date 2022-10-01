from django.shortcuts import render, HttpResponse, redirect
from users import models

# Create your views here.

# 主页
def index(request):
    return render(request, 'index.html')

# 用户列表
def userlist(request):
    user_queryset = models.User.objects.all()
    return render(request, 'userlist.html', locals())

# 注册页面
def register(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        intro = request.POST.get('intro')
        user_obj = models.User.objects.filter(username=username).first()
        if username and password:
            if user_obj:
                return HttpResponse("用户已存在")
            else:
                if len(username) > 32:
                    return HttpResponse("用户名不能超过32个字符")
                elif len(password) > 64:
                    return HttpResponse("密码不能超过64个字符")
                else:
                    user_obj = models.User(username=username,password=password,intro=intro)
                    user_obj.save()
                    return redirect('/userlist/')
        else:
            return HttpResponse("用户或密码不能为空")
    return render(request, 'register.html')

# 登陆页面
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = models.User.objects.filter(username=username).first()
        if user_obj:
            if password == user_obj.password:
                return redirect('/userlist/')
            else:
                return HttpResponse("用户名或密码错误")
        else:
            return HttpResponse("用户名或密码错误")
    return render(request, 'login.html')

# 用户信息管理页面
def edit_user(request):
    edit_id = request.GET.get('user_id')
    edit_obj = models.User.objects.filter(id=edit_id).first()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        intro = request.POST.get('intro')
        if username and password:
            if len(username) > 32:
                return HttpResponse("用户名不能超过32个字符")
            elif len(password) > 64:
                return HttpResponse("密码不能超过64个字符")
            else:
                models.User.objects.filter(id=edit_id).update(username=username,password=password,intro=intro)
                return redirect('/userlist/')
        else:
            return HttpResponse("用户或密码不能为空")
    return render(request, 'edit_user.html', locals())

# 删除用户
def delete_user(request):
    delete_id = request.GET.get('user_id')
    models.User.objects.filter(id=delete_id).delete()
    return redirect('/userlist/')