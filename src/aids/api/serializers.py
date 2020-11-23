from rest_framework import serializers

from aids.models import Aid


class ArrayField(serializers.ListField):
    child = serializers.CharField()

    def __init__(self, choices, *args, **kwargs):

        self.repr_dict = dict(choices)
        super().__init__(*args, **kwargs)

    def to_representation(self, obj):

        representation = [self.repr_dict[choice] for choice in obj]
        return representation


class AidSerializer(serializers.ModelSerializer):
    """Transforms a raw Aid into nice json.

    DON'T TOUCH THIS!

    Instead, do this:
     - create a new Serializer
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

    class Meta:
        model = Aid
        fields = ('id', 'slug', 'url', 'name', 'short_title', 'financers',
                  'instructors', 'description', 'eligibility', 'tags',
                  'perimeter', 'mobilization_steps', 'origin_url',
                  'application_url', 'targeted_audiences', 'aid_types',
                  'destinations', 'start_date', 'predeposit_date',
                  'submission_deadline', 'subvention_rate_lower_bound',
                  'subvention_rate_upper_bound', 'contact', 'recurrence',
                  'project_examples', 'date_created', 'date_updated')

    def get_subvention_rate_lower_bound(self, obj):
        return getattr(obj.subvention_rate, 'lower', None)

    def get_subvention_rate_upper_bound(self, obj):
        return getattr(obj.subvention_rate, 'upper', None)
