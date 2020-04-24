# coding=utf-8
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag


# Register your models here.

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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'owner', 'status', 'created_time', 'operator')
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
        ('额外信息', {
            'classes': ('collapse',),  # CSS样式 ，折叠
            'fields': ('tags',)
        })
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))  # 转到编辑页面
        )

    operator.short_description = '操作'

    def get_queryset(self, request):
        return super(PostAdmin, self).get_queryset(request).filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    class Media:  # 自定义 css样式 ，加载静态资源
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav', 'owner')

    def post_count(self, obj):  # 自定函数，固定的参数，当前行对象obj
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def get_queryset(self, request):
        return super(CategoryAdmin, self).get_queryset(request).filter(owner=request.user)

    def save_model(self, request, obj, form, change):  # 重写save_model方法，将作者设为登录用户
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status', 'owner')

    def get_queryset(self, request):
        return super(TagAdmin, self).get_queryset(request).filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)
