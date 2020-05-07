from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from .models import Post

class LatestPostFeed(Feed):
    feed_type = Rss201rev2Feed
    title="L-Blog"
    link='/rss/'
    description='L-Blog is a blog system power by django'
    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.description
    def item_link(self, item):
        return reverse('post',args=[item.pk])
    def item_extra_kwargs(self, item):
        return {'content_html':self.item_content_html(item)}
    def item_content_html(self,item):
        return item.content_html