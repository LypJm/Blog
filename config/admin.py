from django.contrib import admin

from .models import Link,SideBar
# Register your models here.

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title','href','status','owner','weight','created_time')
    fields = ('title','href','status','weight')

    def get_queryset(self, request):
        return super(LinkAdmin,self).get_queryset(request).filter(owner=request.user)
    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(LinkAdmin,self).save_model(request,obj,form,change)
@admin.register(SideBar)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title','owner','display_type','content','created_time')
    fields = ('title','display_type','content')
    def get_queryset(self, request):
        return super(SideBarAdmin,self).get_queryset(request).filter(owner=request.user)
    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(SideBarAdmin,self).save_model(request,obj,form,change)