from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME


class ExtendedActionsMixin(object):
    # actions that can be executed with no items selected on the admin
    # change list. The filtered queryset displayed to the user will be
    # used instead
    extended_actions = []

    def changelist_view(self, request, extra_context=None):
        # if a extended action is called and there's no checkbox selected,
        # select one with invalid id, to get an empty queryset
        has_action = 'action' in request.POST and \
            request.POST['action'] in self.extended_actions
        if has_action:
            if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                post.update({ACTION_CHECKBOX_NAME: 0})
                request._set_post(post)
        return super(
            ExtendedActionsMixin, self).changelist_view(request, extra_context)

    def get_changelist_instance(self, request):
        """
        Returns a simple ChangeList view instance of the current ModelView.
        (It's a simple instance since we don't populate the actions
        and list filter as expected since those are not used by this class)
        """
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        list_filter = self.get_list_filter(request)
        search_fields = self.get_search_fields(request)
        list_select_related = self.get_list_select_related(request)

        ChangeList = self.get_changelist(request)

        return ChangeList(
            request, self.model, list_display,
            list_display_links, list_filter, self.date_hierarchy,
            search_fields, list_select_related, self.list_per_page,
            self.list_max_show_all, self.list_editable, self, self.sortable_by
        )

    def get_filtered_queryset(self, request):
        """
        Returns a queryset filtered by the URLs parameters
        """
        cl = self.get_changelist_instance(request)
        return cl.get_queryset(request)
