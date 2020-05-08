from django.contrib import admin

from .models import Link,SideBar
from myblog.custom_site import custom_site
from myblog.base_admin import BaseAdmin
# Register your models here.
import xadmin
@xadmin.sites.register(Link)
class LinkAdmin(BaseAdmin):
    list_display = ('title','href','status','owner','weight','created_time')
    fields = ('title','href','status','weight')


@xadmin.sites.register(SideBar)
class SideBarAdmin(BaseAdmin):
    list_display = ('title','owner','display_type','content','created_time')
    fields = ('title','display_type','content')
