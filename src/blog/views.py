from django.views.generic import ListView, DetailView

from blog.models import BlogPost, BlogPostCategory
from stats.utils import log_postviewevent


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

        related_posts_qs = (
            BlogPost.objects.select_related("category")
            .filter(status="published")
            .filter(category=self.object.category)
            .exclude(id=self.object.id)
            .order_by("-date_published")
        )

        context["related_articles"] = related_posts_qs[:5]
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if self.object.status == "published":
            request_ua = self.request.META.get("HTTP_USER_AGENT", "")
            request_referer = self.request.META.get("HTTP_REFERER", "")

            if (
                self.request.user
                and self.request.user.is_authenticated
                and self.request.user.beneficiary_organization
                and self.request.user.beneficiary_organization.organization_type[0]
                in [
                    "commune",
                    "epci",
                    "department",
                    "region",
                    "special",
                    "public_cies",
                    "public_org",
                ]
            ):
                user = self.request.user
                org = user.beneficiary_organization
                log_postviewevent.delay(
                    post_id=self.object.pk,
                    user_pk=user.pk,
                    org_pk=org.pk,
                    request_ua=request_ua,
                    request_referer=request_referer,
                )
            else:
                log_postviewevent.delay(
                    post_id=self.object.pk,
                    request_ua=request_ua,
                    request_referer=request_referer,
                )

        return response
