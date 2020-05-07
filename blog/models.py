# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
import mistune

# Create your models here.
class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    @classmethod
    def get_navs(cls):
        categories=Category.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories=[]
        normal_categories=[]
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {
            'nav':nav_categories,
            'normal':normal_categories
        }

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = verbose_name_plural = '分类'


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "标签"

from django.utils.functional import cached_property
class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    title = models.CharField(max_length=255, verbose_name='标题')
    description = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为Markdown格式')
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    content_html=models.TextField(verbose_name='正文html代码',blank=True,editable=False)

    pv=models.PositiveIntegerField(default=1)
    uv=models.PositiveIntegerField(default=1)

    def save(self, *args,**kwargs):
        self.content_html=mistune.markdown(self.content)
        super().save(*args,**kwargs)
    @cached_property
    def tag(self):
        return ','.join(self.tags.values_list('name',flat=True))

    @classmethod
    def hot_post(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv').only('title','id')
    @classmethod
    def latest_posts(cls):
        queryset=cls.objects.filter(status=Post.STATUS_NORMAL)
        # queryset=cls.objects.all()[:3]
        # print('bbbbbbbbbbbbbbbbbb',queryset)
        return queryset

    @staticmethod
    def get_by_category(category_id):
        try:
            category=Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category=None
            post_list=[]
        else:
            post_list=category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner','category')
        return post_list,category

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag=Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag=None
            post_list=[]
        else:
            post_list=tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner','category')
        return  post_list,tag

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']
