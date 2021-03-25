from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from blog.forms import PostSearchForm
from minisites.mixins import SearchMixin

from blog.models import Post


class PostList(SearchMixin, FormMixin, ListView):
    template_name = 'blog/post_list.html'
    form_class = PostSearchForm
    context_object_name = 'posts'
    paginate_by = 18

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.form.full_clean()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs_categorie = self.request.GET.get('categorie')

        if qs_categorie:
            qs_categorie = qs_categorie.split()
            FilterForm = Post.objects \
                .filter(status='published') \
                .filter(categorie__contains=qs_categorie) \
                .order_by('-date_created')
            return FilterForm
        else:
            return Post.objects \
                .filter(status='published') \
                .order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categorie'] = self.form.cleaned_data.get('categorie', None)
        if context['categorie']:
            context['categorie'] = [Post.POST_CATEGORIES[categorie] for categorie in context['categorie']]  # noqa

        return context


class PostDetail(DetailView):
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
