"""oidc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user.views import user_register, user_login, user_edit_profile, user_oidc, user_activate
from oauth.views import oauth_register_application, oauth_auth, oauth_token, oauth_verify, oauth_auth_callback
from openid.views import oidc_authorize, oidc_authorize_callback, oidc_token, oidc_register_oauth, oidc_user_info, \
    oidc_config
from anime.views import anime_manage, delete_anime, anime_favor, add_fav, delete_fav, edit_fav, search_fav, \
    get_code_from_bangumi, get_code_from_bangumi_callback, import_data_from_bangumi, add_fav_from_bangumi, \
    search_fav_from_bangumi

urlpatterns = [
    path('user/admin/', admin.site.urls),
    path('user/register/', user_register),
    path('user/login/', user_login),
    path('user/edit_profile/', user_edit_profile),
    path('user/activate/', user_activate),
    path('user/authorize/', user_oidc),
    path('oauth/register', oauth_register_application),
    path('oauth/authorize', oauth_auth),
    path('oauth/authorize/callback', oauth_auth_callback),
    path('oauth/token', oauth_token),
    path('oauth/verify', oauth_verify),
    path('oidc/register', oidc_register_oauth),
    path('oidc/authorize', oidc_authorize),
    path('oidc/authorize/callback', oidc_authorize_callback),
    path('oidc/token', oidc_token),
    path('oidc/user_info', oidc_user_info),
    path('.well-known/openid-configuration', oidc_config),
    path('anime/', anime_favor),
    path('anime/admin', anime_manage),
    path('anime/delete', delete_anime),
    path('anime/add_fav', add_fav),
    path('anime/add_fav/bangumi', search_fav_from_bangumi),
    path('anime/add_fav/bangumi/add', add_fav_from_bangumi),
    path('anime/delete_fav', delete_fav),
    path('anime/edit_fav', edit_fav),
    path('anime/search_fav', search_fav),
    path('anime/get_code', get_code_from_bangumi),
    path('anime/get_code/callback', get_code_from_bangumi_callback),
    path('anime/import', import_data_from_bangumi)
]
