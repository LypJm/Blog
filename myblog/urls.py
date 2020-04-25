"""myblog URL Configuration

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
from blog.views import post_detail, post_list
from config.views import link
from .custom_site import custom_site

urlpatterns = [
    path('', post_list, name="index"),
    path('category/<category_id>/', post_list, name="category"),
    path('tag/<tag_id>/', post_list, name="tag"),
    path('post/<post_id>/', post_detail, name="post"),
    path('link/', link, name="link"),

    # path('superadmin/',admin.site.urls),
    path('admin/', custom_site.urls),
]
