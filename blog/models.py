"""
App: blog 下的几个Model都是跟内容直接相关的
每个Model中的Meta类属性:
    配置Model属性，比如Post这个Model，通过Meta配置它的展示名称，排序规则，其他作用之后更新
    Model以及字段类型一起构成了ORM
"""

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    """
    分类：
        id
        name            :名称
        status          :状态
        owner:          :作者, more2one
            owner = models.ForeignKey(User, verbose_name="作者")
        created_time    :创建时间
        is_nav:         :是否置顶导航
        posts: one2more
    知识点：
        1. models.PositiveIntegerField: 正整数
        2. more2one: ForeignKey

    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    )

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "分类"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签
        id              :
        name            :名称
        status          :状态
        created_time    :创建时间
        posts           :文章, more2more
            多对多关系没有在此model中体现
        owner           :作者, more2one
            多对一关系: owner = models.ForeignKey(User, verbose_name="作者")
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    )

    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章
        id
        title           :标题
        desc            :摘要
        content         :正文
        status          :状态
        category        :分类, more2one
            category = models.ForeignKey(Category, verbose_name="分类")
        tag             :标签, more2more
            Tag和Post多对多关系没有在Tag体现，而是放到了这，也就意味着 多对多关系在两者其中一个model体现即可
            tag = models.ManyToManyField(Tag, verbose_name="标签")
        owner           :作者, more2one
            owner = models.ForeignKey(User, verbose_name="作者")
        created_time    :创建时间
        updated_time    :更新时间
        comment         :评论, one2more
            一对多关系没有在此model体现，而是放在了comment.model里的Comment中，使用ForeignKey，
            也就是一对多的关系中，ForeignKey是放在多的model中 △

    知识点:
        1. blank 和 null 区别
            示例：desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
            blank
                设置为True时，字段可以为空。
                设置为False时，字段是必须填写的。
                字符型字段CharField和TextField是用空字符串来存储空值的。

                如果为True，字段允许为空，默认不允许。

            null
                设置为True时，django用Null来存储空值。日期型、时间型和数字型字段不接受空字符串。
                所以设置IntegerField，DateTimeField型字段可以为空时，需要将blank，null均设为True。

                如果为True，空值将会被存储为NULL，默认为False。

                如果想设置BooleanField为空时可以选用NullBooleanField型字段。

            一句话概括
                null 是针对数据库而言，如果 null=True, 表示数据库的该字段可以为空。
                blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填，
                比如 admin 界面下增加 model 一条记录的时候。直观的看到就是该字段不是粗体

        2. help_text：admin模式下帮助文档
        3. Meta类中，操作默认排序
            ordering = ['-id']  # 根据id进行降序排列
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
        (STATUS_DRAFT, "草稿"),
    )

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = models.TextField(verbose_name="正文", help_text="正文必须为MarkDown格式")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name="状态")
    category = models.ForeignKey(Category, verbose_name="分类")
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-id']  # 根据id进行降序排列

    def __str__(self):
        return self.title
