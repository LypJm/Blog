# coding=utf-8
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_time', 'operator')
    list_display_links = []
    list_filter = ['category', ]
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = False
    save_on_top = False

    fields = (
        'category',
        'title',
        'description',
        'status',
        'content',
        'tags',
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))   #转到编辑页面
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav', 'owner')

    def post_count(self, obj):  # 自定函数，固定的参数，当前行对象obj
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):  # 重写save_model方法，将作者设为登录用户
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status', 'owner')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)
