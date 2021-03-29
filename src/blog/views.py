from django.views.generic import ListView, DetailView

from blog.models import Post, PostCategory


class PostList(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 18

    def get_queryset(self):
        if self.kwargs:
            if self.kwargs['category']:
                category = self.kwargs['category']
                category_name = PostCategory.objects \
                    .filter(slug=category) \
                    .values('id') \
                    .distinct()

                return Post.objects \
                    .select_related('category') \
                    .filter(status='published') \
                    .filter(category__in=category_name) \
                    .order_by('-date_created')

        else: 
            return Post.objects \
                .select_related('category') \
                .filter(status='published') \
                .order_by('-date_created')

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            if category is not None:
                context['category'] = PostCategory.objects \
                        .get(slug=category)
            else:
                context['category'] = PostCategory.objects.values('name').distinct()

            return context


class PostDetail(DetailView):
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects \
        .select_related('category') \
        .filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
