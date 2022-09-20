from django.views.generic import ListView, DetailView

from blog.models import BlogPost, BlogPostCategory


class BlogPostList(ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 18

    def get_queryset(self):
        queryset = BlogPost.objects.select_related("category").published()
        category_slug = self.kwargs.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if self.request.GET.get("author"):
            queryset = queryset.filter(author=self.request.GET.get("author"))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = BlogPostCategory.objects.all()
        context["categories"] = categories
        category_slug = self.kwargs.get("category")
        if category_slug:
            context["selected_category"] = categories.filter(slug=category_slug).first()
        return context


class BlogPostDetail(DetailView):
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        """Get the queryset.

        Since we want to enable post preview, we have special cases depending
        on the current user:

         - anonymous or normal users can only see published posts.
         - superusers can see all posts.
        """

        base_qs = BlogPost.objects.select_related("category")

        user = self.request.user
        if user.is_authenticated and user.is_superuser:
            qs = base_qs
        else:
            qs = base_qs.filter(status="published")

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["related_articles"] = (
            BlogPost.objects.select_related("category")
            .filter(status="published")
            .filter(category=self.object.category)
            .exclude(id=self.object.id)
        )
        return context
