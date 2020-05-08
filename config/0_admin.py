from django.contrib import admin

from .models import Link,SideBar
from myblog.custom_site import custom_site
from myblog.base_admin import BaseAdmin
# Register your models here.

@admin.register(Link,site=custom_site)
class LinkAdmin(BaseAdmin):
    list_display = ('title','href','status','owner','weight','created_time')
    fields = ('title','href','status','weight')


@admin.register(SideBar,site=custom_site)
class SideBarAdmin(BaseAdmin):
    list_display = ('title','owner','display_type','content','created_time')
    fields = ('title','display_type','content')
