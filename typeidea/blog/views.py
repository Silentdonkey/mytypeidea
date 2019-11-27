from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import DetailView, ListView

from blog.models import Tag, Post, Category
from config.models import SideBar


class CommonViewMixin:
    '''处理通用的数据'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5  # 每页的数量
    context_object_name = 'post_list'  # 如果不设置此项,在模板中需要使用object_list变量
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    # 拿到要渲染到模板中的数据
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        '''重写queryset,根据分类过滤'''
        queryset = super().get_queryset()  # 拿到数据源
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        '''重写queryset,根据标签过滤'''
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


# def post_list(request, category_id=None, tag_id=None):
#     # 注意Tag和Post是多对多的关系
#     tag = None
#     category = None
#     # 通过在模型Post中定义如下三个静态方法/类方法来重构如下业务代码
#     # 只需要通过tag_id拿到文章列表和tag对象,所以把这个逻辑抽出去作为独立的函数
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_list,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context=context)


class PostDetailView(CommonViewMixin, DetailView):
    # model = Post
    # template_name = 'blog/detail.html'
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

# def post_detail(request, post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all(),
#     }
#     return render(request, 'blog/detail.html', context=context)
