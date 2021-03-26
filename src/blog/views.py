from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.http import HttpResponseRedirect

from minisites.mixins import SearchMixin

from blog.forms import PostSearchForm
from blog.models import Post, PostCategory


class PostListCategory(SearchMixin, FormMixin, ListView):
    template_name = 'blog/post_list.html'
    form_class = PostSearchForm
    context_object_name = 'posts'
    paginate_by = 18

    def get_queryset(self):
        qs_category = self.request.GET.get('category')

        if qs_category:
            category_name = PostCategory.objects \
                .filter(slug=qs_category) \
                .values('id') \
                .distinct()

            FilterForm = Post.objects \
                .select_related('category') \
                .filter(status='published') \
                .filter(category__in=category_name) \
                .order_by('-date_created')
            return FilterForm

        else:
            url = reverse('post_list_view')
            return HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        qs_category = self.request.GET.get('category')
        context = super().get_context_data(**kwargs)
        if qs_category:
            context['category'] = PostCategory.objects \
                    .get(slug=qs_category)

        return context


class PostList(SearchMixin, FormMixin, ListView):
    template_name = 'blog/post_list.html'
    form_class = PostSearchForm
    context_object_name = 'posts'
    paginate_by = 18

    def get_queryset(self):
        return Post.objects \
            .select_related('category') \
            .filter(status='published') \
            .order_by('-date_created')


class PostDetail(DetailView):
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects \
        .select_related('category') \
        .filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
