from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from typeidea import custom_site
from .models import Post, Category, Tag


class PostInline(admin.TabularInline):  # StackedInline 样式不同
    """
    关联内容的管理，但只是偶尔需要考虑
    针对 需要在分类页面直接编辑文章
        但是这种内置（inline）的编辑相关内容的操作更适合字段较少的Model。这里只演示一下它的用法
    """
    fields = ("title", "desc")
    extra = 1  # 控制额外多几个
    model = Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "is_nav", "created_time")
    fields = ("name", "status", "is_nav")

    inlines = [PostInline, ]
    
    def save_model(self, request, obj, form, change):
        """
        通过给 obj.owner赋值，达到自动设置owner的目的。
        :param request: 当前的请求。request.user 就是当前已经登录的用户，如果未登录就是匿名用户。
        :param obj: 当前要保存的对象。
        :param form: 页面提交过来的表单之后的对象
        :param change: 用于标志本次保存的数据是新增的还是更新的。
        :return: 
        """
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        """
        在分类列表页，需要展示该分类下有几篇文章
        :param obj:
        :return:
        """
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "created_time")
    fields = ("name", "status")

    def save_model(self, request, obj, form, change):
        """
        通过给 obj.owner赋值，达到自动设置owner的目的。
        :param request: 当前的请求。request.user 就是当前已经登录的用户，如果未登录就是匿名用户。
        :param obj: 当前要保存的对象。
        :param form: 页面提交过来的表单之后的对象
        :param change: 用于标志本次保存的数据是新增的还是更新的。
        :return:
        """
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    自定义过滤器只展示当前用户分类
    SimpleListFilter类提供了两个属性和两个方法来供我们重写。
        两个属性：
            title           : 展示标题
            parameter_name  : 查询时URL参数的名字  比如: ?parament_name=1
        两个方法：
            lookups     : 返回要展示的内容和查询用的id（就是上面Query用的）
            queryset    : 根据URL Query 的内容返回列表页数据。比如如果URL最后的Query是?owner_category=1，
                        那么这里拿到的 self.value()就是1，此时就会根据1来过滤QuerySet ，也就是post 的数据集
    """
    title = "分类过滤器"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list("id", "name")

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site.custom_site)  # 多套admin后台时，加入site配置
class PostAdmin(admin.ModelAdmin):
    """
    各配置介绍：
    list_display: 用来配置列表页面展示哪些字段
    list_display_links: 配置哪些字段可以作为链接，点击它们，可以进入编辑页面
    list_filter: 配置页面过滤器， 需要通过哪些字段来过滤列表页
    search_fields: 配置搜索字段
    actions_on_top: 动作相关配置，是否展示在顶部
    actions_on_bottom: 动作相关配置，是否展示在底部
    save_on_top: 保存、编辑、编辑并保存新建按钮是否在顶部显示
    """
    list_display = [
        "title", "category", "status",
        "created_time", "operator", "owner"
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter, ]
    search_fields = ["title", "category__name"]

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
        # 'owner'
    )

    # 自定义后台Form， 希望编辑文章描述字段能够以textarea展示
    from .adminforms import PostAdminForm
    form = PostAdminForm

    def operator(self, obj):
        """
        自定义方法，如果想要展示自定义字段，就这么处理。

        :param obj: 当前的对象，列表页中的每一行数据都对应数据表中的一条数据，也对应Model的一个实例。
        :return:
            自定义函数可以返回HTML，但是需要通过 format_html函数处理，reverse是根据名称解析出URL地址
        """
        return format_html(
            '<a href="{}"编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id, ))
        )
    operator.short_description = "操作"  # 制定表头的展示文案

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        """
        定制文章管理页，只显示属于自己的文章
            小技巧：关于数据过滤的部分，只要找到数据源在哪，也就是QuerySet最终在哪生成，然后对其过滤即可
        :param request:
        :return:
        """
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
# class CategoryAdmin(admin.ModelAdmin):
#     inlines = ["PostInline", ]
