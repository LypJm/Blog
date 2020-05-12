"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from blog.views import post_detail, post_list,LinkView,IndexView,CategoryView,TagView,PostDetailView,SearchView,AuthorView
from comment.views import CommentView
from config.views import link
from myblog.settings import base
from .custom_site import custom_site
from django.contrib.sitemaps import views as sitemap_views
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
import xadmin
from .autocomplete import CategoryAutocomplete,TagAutocomplete
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('category/<category_id>/', CategoryView.as_view(), name="category"),
    path('tag/<tag_id>/', TagView.as_view(), name="tag"),
    path('post/<post_id>/', PostDetailView.as_view(), name="post"),
    path('link/', link, name="link"),
    path('search/',SearchView.as_view(),name='search'),
    path('author/<author_id>/',AuthorView.as_view(),name='author'),
    path('links/',LinkView.as_view(),name='link'),
    path('comment/',CommentView.as_view(),name='comment'),

    path('category-autocomplete/',CategoryAutocomplete.as_view(),name='category-autocomplete'),
    path('tag-autocomplete/',TagAutocomplete.as_view(),name='tag-autocomplete'),

    path('ckeditor/',include('ckeditor_uploader.urls')),

    path(r'rss|feed/',LatestPostFeed(),name='rss'),
    path(r'sitemap.xml',sitemap_views.sitemap,{'sitemaps':{'posts':PostSitemap}}),
    path('admin/',xadmin.site.urls,name='xadmin'),
    # path('superadmin/',admin.site.urls),
    # path('admin/', custom_site.urls),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if base.DEBUG:
    import debug_toolbar
    urlpatterns.append(path(r"__debug__/", include(debug_toolbar.urls)))