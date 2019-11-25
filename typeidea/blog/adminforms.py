# -*- coding: utf-8 -*

from django import forms

# 用作后台管理的Form,与前台针对用户输入进行处理的Form(forms.py)区分开来
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)

