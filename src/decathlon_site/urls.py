"""decathlon_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from game.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('signup/', signup, name="signup"),
    path('createuser/', createUser, name="createuser"),
    path('logout/', logout, name="logout"),
    path('javelot/settings/', javelot_settings, name="javelot_settings"),
    path('javelot/play/', javelot_play, name="javelot_play"),
    path('javelot/roll_dice/', roll_dice, name="roll-dice"),
    re_path(r'^javelot/result/(?P<game_id>[0-9]+)/$', result, name="result")
]
