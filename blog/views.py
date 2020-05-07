from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category, Tag
from config.models import SideBar, Link
from django.views.generic import View, ListView, DetailView
from django.db.models import F


# Create your views here.
# 类视图
class CommonViewMixin:
    def get_context_data(self, **kwargs):
        # print(self.kwargs)
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebar': SideBar.get_all()
        })
        context.update({
            'link_list': Link.objects.filter(status=Link.STATUS_NORMAL)
        })
        context.update(Category.get_navs())
        # print(context)
        return context

class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            "category": category
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # print(self.kwargs)

        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update(
            {
                'tag': tag
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        # print(queryset)
        return queryset.filter(tags__id=tag_id)

from comment.forms import CommentForm
from comment.models import Comment
from django.core.cache import cache
from datetime import date

class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    def get(self, request, *args, **kwargs):
        response=super().get(request,*args,**kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv=False
        increase_uv=False
        uid=self.request.uid
        pv_key='pv:%s:%s'%(uid,self.request.path)
        uv_key='uv:%s:%s:%s'%(uid,str(date.today()),self.request.path)
        if not cache.get(pv_key):
            increase_pv=True
            cache.set(pv_key,1,1*60)
        if not cache.get(uv_key):
            increase_uv=True
            cache.set(uv_key,1,24*60*60)
        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv')+1)

    # def get_context_data(self, **kwargs):
    #     context=super().get_context_data(**kwargs)
    #     context.update(
    #         {
    #             'comment_form':CommentForm,
    #             'comment_list':Comment.get_by_target(self.request.path)
    #          }
    #     )
    #     return context

from django.db.models import Q
class SearchView(IndexView):
    def get_queryset(self):
        queryset=super().get_queryset()
        keyword=self.request.GET.get('keyword')
        if not keyword:
            return queryset
        else:
            return queryset.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword','') #如果keyword为空，则返回‘’
        })

        return context

class AuthorView(IndexView):
    def get_queryset(self):
        queryset=super().get_queryset()
        author_id=self.kwargs.get('author_id')
        return queryset.filter(owner_id=author_id)

class LinkView(CommonViewMixin,ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'



# 函数视图
def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None
    # if tag_id:
    #     try:
    #         tag = Tag.objects.get(id=tag_id)
    #     except Tag.DoesNotExist:
    #         post_list = []
    #     else:
    #         post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    # else:
    #     post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
    #     if category_id:
    #         try:
    #             category=Category.objects.get(id=category_id)
    #         except Category.DoesNotExist:
    #             category=None
    #         else:
    #             post_list.objects.filter(category_id=category_id)
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()
    context = {
        'post_list': post_list,
        'tag': tag,
        'category': category,
        'sidebar': SideBar.get_all()
    }
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    context = {
        'post': post,
        'sidebar': SideBar.get_all()
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)
