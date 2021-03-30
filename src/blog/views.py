from django.views.generic import ListView, DetailView

from blog.models import BlogPost, BlogPostCategory


class BlogPostList(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 18

    def get_queryset(self):
        queryset = BlogPost.objects.select_related('category').published()
        category_slug = self.kwargs.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = BlogPostCategory.objects.all()
        context['categories'] = categories
        category_slug = self.kwargs.get('category')
        if category_slug:
            context['selected_category'] = \
                categories.filter(slug=category_slug).first()
        return context


class BlogPostDetail(DetailView):
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    queryset = BlogPost.objects \
        .select_related('category') \
        .filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
