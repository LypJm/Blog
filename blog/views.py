from django.shortcuts import render
from django.http import HttpResponse
from .models import Post,Category,Tag
from config.models import SideBar,Link
# Create your views here.

def post_list(request,category_id=None,tag_id=None):
    tag=None
    category=None
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
        post_list,tag=Post.get_by_tag(tag_id)
    elif category_id:
        post_list,category=Post.get_by_category(category_id)
    else:
        post_list=Post.latest_posts()
    context={
        'post_list':post_list,
        'tag':tag,
        'category':category,
        'sidebar':SideBar.get_all()
    }
    context.update(Category.get_navs())
    return render(request,'blog/list.html',context=context)

def post_detail(request,post_id):
    try:
        post=Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post=None
    context={
        'post':post,
        'sidebar':SideBar.get_all()
    }
    context.update(Category.get_navs())
    return render(request,'blog/detail.html',context=context)