from django.views.generic import ListView, DetailView

from blog.models import Post


class PostList(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 18

    def get_queryset(self):
        qs = Post.objects.all()
        return qs


class PostDetail(DetailView):
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
