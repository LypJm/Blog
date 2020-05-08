# coding=utf-8
from django.contrib import admin
from myblog.base_admin import BaseAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from myblog.custom_site import custom_site

# Register your models here.

#查看日志的页面 admin组件才使用，而xadmin中已配置好展示逻辑，所以不用以下代码
# @admin.register(LogEntry,site=custom_site)
# class LogAdmin(admin.ModelAdmin):
#     list_display = ["object_repr",'object_id','action_flag','user','change_message']

# 在同一页面编辑关联数据
class PostInline(admin.TabularInline):
    fields = ('title', 'description', 'owner')
    extra = 1
    model = Post

class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseAdmin):
    form = PostAdminForm
    list_display = ('title', 'category' ,'owner', 'status', 'created_time', 'operator')
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = False
    save_on_top = False
    # filter_vertical = ('tags',)   #针对多对多 字段的样式配置
    filter_horizontal = ('tags',)
    # fields = (
    #     'category',
    #     'title',
    #     # 'owner',
    #     'description',
    #     'status',
    #     'content',
    #     'tags',
    # )
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': ('title', 'category', 'status')
        }),
        ('内容', {
            'fields': ('description', 'content')
        }),
        ('标签', {
            # 'classes': ('collapse',),  # CSS样式 ，折叠
            'fields': ('tags',)
        })
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))  # 转到编辑页面
        )

    operator.short_description = '操作'

    class Media:  # 自定义 css样式 ，加载静态资源
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseAdmin):
    list_display = ('name', 'status', 'owner', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')
    inlines = [PostInline, ]

    def post_count(self, obj):  # 自定函数，固定的参数，当前行对象obj
        return obj.post_set.count()

    post_count.short_description = '文章数量'

@admin.register(Tag, site=custom_site)
class TagAdmin(BaseAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')
