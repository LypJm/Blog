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
from blog.views import post_detail, post_list,IndexView,CategoryView,TagView,PostDetailView
from config.views import link
from .custom_site import custom_site

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('category/<category_id>/', CategoryView.as_view(), name="category"),
    path('tag/<tag_id>/', TagView.as_view(), name="tag"),
    path('post/<post_id>/', PostDetailView.as_view(), name="post"),
    path('link/', link, name="link"),
    # path('superadmin/',admin.site.urls),
    path('admin/', custom_site.urls),
]
