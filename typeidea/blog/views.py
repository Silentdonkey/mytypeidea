from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from blog.models import Tag, Post, Category
from config.models import SideBar


def post_list(request, category_id=None, tag_id=None):
    # 注意Tag和Post是多对多的关系
    tag = None
    category = None
    # 通过在模型Post中定义如下三个静态方法/类方法来重构如下业务代码
    # 只需要通过tag_id拿到文章列表和tag对象,所以把这个逻辑抽出去作为独立的函数
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()
    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
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
        'sidebars': SideBar.get_all(),
    }
    return render(request, 'blog/detail.html', context=context)
