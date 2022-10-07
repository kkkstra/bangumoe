import json, requests
import secrets
import string

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


def add_fav(request):
    if request.method == "POST":
        username = request.POST.get("username")
        aid = request.POST.get("aid")
        title = request.POST.get("title")
        episode = request.POST.get("episode")
        director = request.POST.get("director")
        status = request.POST.get("type")
        score = request.POST.get("score")
        comment = request.POST.get("comment")
        fav_obj = models.UserFavorAnime(username=username, aid=aid, title=title, episode=episode, director=director,
                                        type=status, score=score, comment=comment)
        fav_obj.save()
        return redirect("/anime/")
    username = request.GET.get("username")
    aid = request.GET.get("aid")
    return render(request, 'anime/add_fav.html', locals())


def delete_fav(request):
    iid = request.GET.get("id")
    models.UserFavorAnime.objects.filter(id=iid).delete()
    return redirect('/anime/')


def edit_fav(request):
    if request.method == "POST":
        iid = request.POST.get("id")
        username = request.POST.get("username")
        aid = request.POST.get("aid")
        status = request.POST.get("type")
        score = request.POST.get("score")
        comment = request.POST.get("comment")
        fav_obj = models.UserFavorAnime.objects.filter(id=iid).first()
        title = fav_obj.title
        episode = fav_obj.episode
        director = fav_obj.director
        models.UserFavorAnime.objects.filter(username=username, aid=aid).update(type=status, score=score,
                                                                                comment=comment)
        return redirect("/anime/")
    else:
        iid = request.GET.get("id")
        fav_obj = models.UserFavorAnime.objects.filter(id=iid).first()
        username = fav_obj.username
        aid = fav_obj.aid
        # anime_obj = models.AnimeData.objects.filter(id=aid).first()
        title = fav_obj.title
        episode = fav_obj.episode
        director = fav_obj.director
        status = fav_obj.type
        score = fav_obj.score
        comment = fav_obj.comment
        return render(request, "anime/edit_favor.html", locals())


def search_fav(request):
    res = False
    if request.method == "POST":
        username = request.POST.get("username")
        keywrd = request.POST.get("keywrd")
        res = True
        fav_list = models.UserFavorAnime.objects.filter(
            Q(username=username) & (Q(title__icontains=keywrd) | Q(director__icontains=keywrd)
                                    | Q(comment__icontains=keywrd)))
        return render(request, 'anime/search_fav.html', locals())
    username = request.GET.get("username")
    return render(request, 'anime/search_fav.html', locals())


def generate_state():
    alphabet = string.ascii_letters + string.digits
    while True:
        state = ''.join(secrets.choice(alphabet) for i in range(16))
        if (any(c.islower() for c in state)
                and any(c.isupper() for c in state)
                and any(c.isupper() for c in state)):
            break
    return state


# 从bangumi获取Authorization Code
def get_code_from_bangumi(request):
    username = request.GET.get("username")
    response_type = "code"
    client_id = "bgm2439633e8ae648eb0"
    state = generate_state()
    # 将state和username绑定
    stu_obj = models.StateToUsername(state=state, username=username)
    stu_obj.save()
    url = "https://bgm.tv/oauth/authorize?response_type=%s&client_id=%s&state=%s" % (response_type, client_id, state)
    # res = requests.get(url)
    return redirect(url)


# 获取access token
def get_code_from_bangumi_callback(request):
    grant_type = "authorization_code"
    client_id = "bgm2439633e8ae648eb0"
    client_secret = "3acb8eab79bf09d510be0776162e9ca3"
    code = request.GET.get("code")
    redirect_uri = "http://127.0.0.1:8001/anime/get_code/callback"
    state = request.GET.get("state")
    username = models.StateToUsername.objects.filter(state=state).first().username
    headers = {'User-Agent': 'kkkstra/bangumoue'}
    data = {"grant_type": grant_type, "client_id": client_id, "client_secret": client_secret, "code": code,
            "redirect_uri": redirect_uri, "state": state}
    res = requests.post("https://bgm.tv/oauth/access_token", json=data, headers=headers)
    js_res = json.loads(res.content.decode())
    access_token = js_res.get("access_token")
    refresh_token = js_res.get("refresh_token")
    uid = js_res.get("user_id")
    # 将token与uid存储起来
    utt_obj = models.UsernameToToken.objects.filter(username=username).first()
    if utt_obj:
        models.UsernameToToken.objects.filter(username=username).update(access_token=access_token,
                                                                        refresh_token=refresh_token, uid=uid)
    else:
        utt_obj = models.UsernameToToken(username=username, access_token=access_token, refresh_token=refresh_token,
                                         uid=uid)
        utt_obj.save()
    host = "http://" + request.get_host()
    url = host + "/anime/import?username=%s" % username
    return redirect(url)


# 从bangumi导入数据
def import_data_from_bangumi(request):
    if request.method == "POST":
        username = request.GET.get("username")
        utt_obj = models.UsernameToToken.objects.filter(username=username).first()
        access_token = utt_obj.access_token
        uid = utt_obj.uid
        headers = {'Authorization': 'Bearer {}'.format(access_token),
                   'User-Agent': 'kkkstra/bangumoue'}
        url = "https://api.bgm.tv/v0/users/%s/collections" % str(uid)
        res = requests.get(url, headers=headers)
        js_res = json.loads(res.content.decode())
        data = js_res.get("data")
        for data_obj in data:
            aid = data_obj.get("subject_id")
            subject = data_obj.get("subject")
            title = subject.get("name_cn")
            if title == "":
                title = subject.get("name")
            episode = subject.get("eps")
            # 获取导演信息
            url = "https://api.bgm.tv/v0/subjects/%s/persons" % str(aid)
            headers = {'User-Agent': 'kkkstra/bangumoue'}
            person_res = requests.get(url, headers=headers)
            person_js_res = json.loads(person_res.content.decode())
            # director = ""
            # return HttpResponse(person_res.content.decode())
            director = ""
            for i in range(0, len(person_js_res) - 1):
                if person_js_res[i].get("relation") == "总导演" or person_js_res[i].get("relation") == "导演":
                    director = person_js_res[i].get("name")
                    break
            status = data_obj.get("type")
            score = data_obj.get("rate")
            comment = data_obj.get("comment")
            fav_obj = models.UserFavorAnime.objects.filter(username=username, aid=aid).first()
            if fav_obj:
                models.UserFavorAnime.objects.filter(username=username, aid=aid).update(type=status, score=score,
                                                                                        comment=comment)
            else:
                fav_obj = models.UserFavorAnime(username=username, aid=aid, type=status, score=score, comment=comment,
                                                title=title, episode=episode, director=director)
                fav_obj.save()
        return redirect("/anime")
    username = request.GET.get("username")
    utt_obj = models.UsernameToToken.objects.filter(username=username).first()
    access_token = utt_obj.access_token
    uid = utt_obj.uid
    headers = {'Authorization': 'Bearer {}'.format(access_token),
               'User-Agent': 'kkkstra/bangumoue'}
    url = "https://api.bgm.tv/v0/users/%s/collections" % str(uid)
    res = requests.get(url, headers=headers)
    js_res = json.loads(res.content.decode())
    data = js_res.get("data")
    # return HttpResponse(res.content.decode())
    return render(request, 'anime/import.html', locals())


def search_fav_from_bangumi(request):
    if request.method == "POST":
        username = request.POST.get("username")
        keywrd = request.POST.get("keywrd")
        # 获取搜索内容
        url = "https://api.bgm.tv/v0/search/subjects"
        headers = {'content-type': "application/json", 'User-Agent': 'kkkstra/bangumoue'}
        body = {"keyword": keywrd, "filter": {"type": [2]}}
        res = requests.post(url, data=json.dumps(body), headers=headers)
        js_res = json.loads(res.content.decode())
        search_list = js_res.get("data")
        return render(request, 'anime/search_fav_from_bangumi.html', locals())
    username = request.GET.get("username")
    return render(request, 'anime/search_fav_from_bangumi.html', locals())


def add_fav_from_bangumi(request):
    if request.method == "POST":
        username = request.POST.get("username")
        aid = request.POST.get("aid")
        title = request.POST.get("title")
        episode = request.POST.get("episode")
        director = request.POST.get("director")
        status = request.POST.get("type")
        score = request.POST.get("score")
        comment = request.POST.get("comment")
        fav_obj = models.UserFavorAnime(username=username, aid=aid, title=title, episode=episode, director=director,
                                        type=status, score=score, comment=comment)
        fav_obj.save()
        return redirect("/anime/")
    username = request.GET.get("username")
    aid = request.GET.get("aid")
    # 从bangumi上获取相关信息
    headers = {'User-Agent': 'kkkstra/bangumoue'}
    url = "https://api.bgm.tv/v0/subjects/%s" % str(aid)
    res = requests.get(url, headers=headers)
    js_res = json.loads(res.content.decode())
    title = js_res.get("name_cn")
    if title == "":
        title = js_res.get("name")
    episode = js_res.get("eps")
    # 获取导演信息
    url = "https://api.bgm.tv/v0/subjects/%s/persons" % str(aid)
    headers = {'User-Agent': 'kkkstra/bangumoue'}
    person_res = requests.get(url, headers=headers)
    person_js_res = json.loads(person_res.content.decode())
    # director = ""
    # return HttpResponse(person_res.content.decode())
    director = ""
    for i in range(0, len(person_js_res) - 1):
        if person_js_res[i].get("relation") == "总导演" or person_js_res[i].get("relation") == "导演":
            director = person_js_res[i].get("name")
            break
    return render(request, 'anime/add_fav_from_bangumi.html', locals())
