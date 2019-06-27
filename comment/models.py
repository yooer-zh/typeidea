"""
评论部分单独拎出来
评论可以使完全独立的模块，如果往大了做，可以作为独立的系统，比如：畅言、Disqus等产品
可以把它耦合到文章上，创建一个一对多的关系，
当然，也可以耦合松一点，评论功能完全独立，只关心针对哪个页面（或URL）来评论。
这样做的好处是：产品可以增加新的页面类型，比如友链页增加评论或者文章列表页增加评论，只关心URL，而不用关心要评论的对象是什么

此处暂时按照耦合的方式来做，即通过外键关联Post的方式，后面再做修改。
"""
from django.db import models

from blog.models import Post

# Create your models here.


class Comment(models.Model):
    """

    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    )

    target = models.ForeignKey(Post, verbose_name="评论目标")
    content = models.CharField(max_length=2000, verbose_name="内容")
    nickname = models.CharField(max_length=50, verbose_name="昵称")
    website = models.URLField(verbose_name="网站")
    email = models.EmailField(verbose_name="邮箱")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "评论"
