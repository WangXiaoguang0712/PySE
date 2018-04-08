"""PySE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from myse import views
from myse import view_json

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'news_index/', views.news_index),
    path(r'news_list/', views.news_list),
    path(r'news_detail/', views.news_detail),
    path(r'news_search/', views.news_search),
    path(r'news_searched/', views.news_searched),
    path(r'grab_web/', view_json.grab_web),
    path(r'handle/', view_json.handle),

    path(r'test/', views.sayHello),

]
