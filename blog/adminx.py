# coding=utf-8
from django.contrib import admin
from myblog.base_admin import BaseAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from myblog.custom_site import custom_site

from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter
import xadmin
# import xadmin.util

# Register your models here.

# 在同一页面编辑关联数据
class PostInline():
    form_layout=(
        Container(
            Row('title','description','owner'),
        )
    )
    extra = 1
    model = Post

class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name=='category'
    def __init__(self,field, request, params, model, admin_view, field_path):
        super().__init__(field, request, params, model, admin_view, field_path)
        self.lookup_choices=Category.objects.filter(owner=request.user).values_list('id','name')

manager.register(CategoryOwnerFilter,take_priority=True)

@xadmin.sites.register(Post)
class PostAdmin(BaseAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'owner', 'status', 'created_time', 'operator')
    list_display_links = []
    list_filter = ["category"]
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = False
    save_on_top = False
    # filter_vertical = ('tags',)   #针对多对多 字段的样式配置
    filter_horizontal = ('tags',)

    form_layout = (
        Fieldset(
            '基础配置', Row('title', 'category'),
            'status',
            'tags', ),
        Fieldset('内容',
                 'description', 'content',
                 )
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))  # 转到编辑页面
        )

    operator.short_description = '操作'

    # @property
    # def media(self):    # 自定义 css样式 ，加载静态资源 ,xadmin是基于Bootstrap的，引入以下样式会导致样式冲突，而发生错误
    #     media=super().media
    #     media.add_css( {'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",)})
    #     media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',])
    #     return media

@xadmin.sites.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('name', 'status', 'owner', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')
    inlines = [PostInline, ]

    def post_count(self, obj):  # 自定函数，固定的参数，当前行对象obj
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')
