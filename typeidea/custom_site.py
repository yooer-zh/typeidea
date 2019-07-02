"""
大部分情况下， 一个site对应一个站点，这就像上面所有操作最终都反映在一个后台。
当然，也可以通过定制site来实现一个系统对外提供多套admin后台的逻辑。

"""
from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    """
    继承AdminSite来定义自己的site
    """
    site_header = "Typeidea"
    site_title = "Typeidea管理后台"
    index_title = "首页"


custom_site = CustomSite(name='cus_admin')
