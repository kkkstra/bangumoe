import json, requests

from django.http import HttpResponse
from django.shortcuts import render, redirect
from anime import models
from django.db.models import Q


# Create your views here.

def anime_manage(request):
    if request.method == "GET":
        title = request.GET.get("title")
        episode = request.GET.get("episode")
        director = request.GET.get("director")
        if title and episode and director:
            anime_obj = models.AnimeData(title=title, episode=episode, director=director)
            anime_obj.save()
            anime_list = models.AnimeData.objects.all()
            return render(request, 'anime/anime_admin.html', locals())
        else:
            return render(request, 'anime/anime_admin_login.html', locals())
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == "admin" and password == "admin":
            anime_list = models.AnimeData.objects.all()
            return render(request, 'anime/anime_admin.html', locals())
        else:
            return render(request, 'anime/anime_admin_login.html', locals())


def delete_anime(request):
    delete_id = request.GET.get('anime_id')
    models.AnimeData.objects.filter(id=delete_id).delete()
    return redirect('/anime/admin')


# 番剧收藏
def anime_favor(request):
    if request.method == "POST":
        # 登录验证
        username = request.POST.get("username")
        password = request.POST.get("password")
        host = "http://" + request.get_host()
        headers = {'content-type': "application/json"}
        body = {"username": username, "password": password}
        res = requests.post(host + "/user/login/", data=json.dumps(body), headers=headers)
        js_res = json.loads(res.content.decode())
        success = js_res.get("success")
        if success:
            anime_list = models.AnimeData.objects.all()
            favor_list = models.UserFavorAnime.objects.filter(username=username)
            return render(request, 'anime/favor.html', locals())
    return render(request, 'anime/favor_login.html', locals())


def delete_fav(request):
    aid = request.GET.get('aid')
    username = request.GET.get('username')
    models.UserFavorAnime.objects.filter(id=aid, username=username).delete()
    return redirect('/anime/')


def edit_fav(request):
    if request.method == "POST":
        username = request.POST.get("username")
        aid = request.POST.get("aid")
        status = request.POST.get("type")
        score = request.POST.get("score")
        comment = request.POST.get("comment")
        anime_obj = models.AnimeData.objects.filter(id=aid).first()
        if anime_obj:
            title = anime_obj.title
            episode = anime_obj.episode
            director = anime_obj.director
            fav_obj = models.UserFavorAnime.objects.filter(username=username, aid=aid).first()
            if fav_obj:
                models.UserFavorAnime.objects.filter(username=username, aid=aid).update(type=status, score=score,
                                                                                        comment=comment)
            else:
                fav_obj = models.UserFavorAnime(username=username, aid=aid, type=status, score=score, comment=comment,
                                                title=title, episode=episode, director=director)
                fav_obj.save()
            return redirect("/anime/")
        else:
            return HttpResponse(username)
    else:
        username = request.GET.get("username")
        aid = request.GET.get("aid")
        anime_obj = models.AnimeData.objects.filter(id=aid).first()
        title = anime_obj.title
        episode = anime_obj.episode
        director = anime_obj.director
        fav_obj = models.UserFavorAnime.objects.filter(username=username, aid=aid).first()
        if fav_obj:
            status = fav_obj.type
            score = fav_obj.score
            comment = fav_obj.comment
        else:
            status = 1
            score = 5
            comment = ""
        return render(request, "anime/edit_favor.html", locals())


def search_fav(request):
    res = False
    if request.method == "POST":
        username = request.POST.get("username")
        keywrd = request.POST.get("keywrd")
        res = True
        fav_list = models.UserFavorAnime.objects.filter(Q(username=username) & (Q(title__icontains=keywrd) | Q(director__icontains=keywrd)
                                                       | Q(comment__icontains=keywrd)))
        return render(request, 'anime/search_fav.html', locals())
    username = request.GET.get("username")
    return render(request, 'anime/search_fav.html', locals())