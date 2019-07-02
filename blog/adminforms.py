"""
后台管理的Form，为了和前台针对用户输入的Form区分
自定义form，比如希望文章描述字段能够以textarea展示
"""
from django import forms


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label="摘要", required=False)
