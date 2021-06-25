from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from aids.models import Aid


class ArrayField(serializers.ListField):
    child = serializers.CharField()

    def __init__(self, choices, *args, **kwargs):
        self.repr_dict = dict(choices)
        super().__init__(*args, **kwargs)

    def to_representation(self, obj):
        representation = [self.repr_dict[choice] for choice in obj]
        return representation


class BaseAidSerializer(serializers.ModelSerializer):
    """Transforms a raw Aid into nice json.

    DON'T TOUCH THIS!

    Instead, do this:
     - create a new Serializer
     - make sure `AidSerializerLatest` inherits from the new serializer
     - bump the default api version in settings
     - update `aids.api.views.AidViewSet.get_serializer_class`
     - update the /data/ documentation page

    """

    url = serializers.URLField(source='get_absolute_url')
    financers = serializers.StringRelatedField(many=True)
    instructors = serializers.StringRelatedField(many=True)
    perimeter = serializers.StringRelatedField()
    mobilization_steps = ArrayField(Aid.STEPS)
    targeted_audiences = ArrayField(Aid.AUDIENCES)
    aid_types = ArrayField(Aid.TYPES)
    destinations = ArrayField(Aid.DESTINATIONS)
    recurrence = serializers.CharField(source='get_recurrence_display')
    subvention_rate_lower_bound = serializers.SerializerMethodField(
        'get_subvention_rate_lower_bound')
    subvention_rate_upper_bound = serializers.SerializerMethodField(
        'get_subvention_rate_upper_bound')
    programs = serializers.StringRelatedField(many=True)

    def get_subvention_rate_lower_bound(self, obj):
        return getattr(obj.subvention_rate, 'lower', None)

    def get_subvention_rate_upper_bound(self, obj):
        return getattr(obj.subvention_rate, 'upper', None)

    class Meta:
        model = Aid


class AidSerializer10(BaseAidSerializer):

    class Meta(BaseAidSerializer.Meta):
        fields = ('id', 'slug', 'url', 'name', 'short_title', 'financers',
                  'instructors', 'description', 'eligibility',
                  'perimeter', 'mobilization_steps', 'origin_url',
                  'application_url', 'targeted_audiences', 'aid_types',
                  'destinations', 'start_date', 'predeposit_date',
                  'submission_deadline', 'subvention_rate_lower_bound',
                  'subvention_rate_upper_bound', 'contact', 'recurrence',
                  'project_examples', 'date_created', 'date_updated')


class AidSerializer11(BaseAidSerializer):
    """
    Add 'programs'.
    """

    class Meta(BaseAidSerializer.Meta):
        fields = ('id', 'slug', 'url', 'name', 'short_title', 'financers',
                  'instructors', 'programs', 'description', 'eligibility',
                  'perimeter', 'mobilization_steps', 'origin_url',
                  'application_url', 'targeted_audiences', 'aid_types',
                  'destinations', 'start_date', 'predeposit_date',
                  'submission_deadline', 'subvention_rate_lower_bound',
                  'subvention_rate_upper_bound', 'contact', 'recurrence',
                  'project_examples', 'date_created', 'date_updated')


class CategoryRelatedField(serializers.StringRelatedField):

    def to_representation(self, value):
        return f'{value.theme}|{value}'


class AidSerializer12(BaseAidSerializer):
    """
    Add 'categories'.
    """

    categories = CategoryRelatedField(
        many=True,
        label=_('Theme and category, separated by « | ».'),
        help_text=_('E.g: "Nature / environnement|Qualité de l\'air"'))

    class Meta(BaseAidSerializer.Meta):
        fields = ('id', 'slug', 'url', 'name', 'short_title', 'financers',
                  'instructors', 'programs', 'description', 'eligibility',
                  'perimeter', 'mobilization_steps', 'origin_url',
                  'categories',
                  'application_url', 'targeted_audiences', 'aid_types',
                  'destinations', 'start_date', 'predeposit_date',
                  'submission_deadline', 'subvention_rate_lower_bound',
                  'subvention_rate_upper_bound', 'contact', 'recurrence',
                  'project_examples', 'date_created', 'date_updated')


class AidSerializer13(BaseAidSerializer):
    """
    Add 'loan_amount' and 'recoverable_advance_amount' fields.
    Remove 'tags'.
    """

    categories = CategoryRelatedField(
        many=True,
        label=_('Theme and category, separated by « | ».'),
        help_text=_('E.g: "Nature / environnement|Qualité de l\'air"'))

    class Meta(BaseAidSerializer.Meta):
        fields = ('id', 'slug', 'url', 'name', 'short_title', 'financers',
                  'instructors', 'programs', 'description', 'eligibility',
                  'perimeter', 'mobilization_steps', 'origin_url',
                  'categories',
                  'application_url', 'targeted_audiences', 'aid_types',
                  'destinations', 'start_date', 'predeposit_date',
                  'submission_deadline', 'subvention_rate_lower_bound',
                  'subvention_rate_upper_bound', 'loan_amount',
                  'recoverable_advance_amount', 'contact', 'recurrence',
                  'project_examples', 'date_created', 'date_updated')


class AidSerializerLatest(AidSerializer13):
    pass
