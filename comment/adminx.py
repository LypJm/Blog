from django.contrib import admin

from .models import Comment
from myblog.custom_site import custom_site
# Register your models here.
import xadmin
@xadmin.sites.register(Comment)
class CommentAdmin():
    list_display = ('target','nickname','content','website','created_time')
