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


class BaseAidSerializer(serializers.ModelSerializer):
    """Transforms a raw Aid into nice json.

    DON'T TOUCH THIS!

    Instead, do this:
     - create a new Serializer
     - make sure `AidSerializerLatest` inherits from the new serializer
     - bump the default API version in the settings
     - update `aids.api.views.AidViewSet.get_serializer_class`
     - update the documentation : src/template/data/doc.html & src/core/api/doc.py

    """

    url = serializers.URLField(
        source="get_absolute_url", label="URL sur Aides-territoires"
    )
    financers = serializers.StringRelatedField(
        many=True, label=Aid._meta.get_field("financers").verbose_name
    )
    instructors = serializers.StringRelatedField(
        many=True, label=Aid._meta.get_field("instructors").verbose_name
    )
    perimeter = serializers.StringRelatedField(
        label=Aid._meta.get_field("perimeter").verbose_name,
        help_text=Aid._meta.get_field("perimeter").help_text,
    )
    programs = serializers.StringRelatedField(
        many=True, label=Aid._meta.get_field("programs").verbose_name
    )
    mobilization_steps = ArrayField(
        Aid.STEPS, label=Aid._meta.get_field("mobilization_steps").verbose_name
    )
    targeted_audiences = ArrayField(
        Aid.AUDIENCES, label=Aid._meta.get_field("targeted_audiences").verbose_name
    )
    aid_types = ArrayField(
        Aid.TYPES, label=Aid._meta.get_field("aid_types").verbose_name
    )
    destinations = ArrayField(
        Aid.DESTINATIONS, label=Aid._meta.get_field("destinations").verbose_name
    )
    recurrence = serializers.CharField(
        source="get_recurrence_display",
        label=Aid._meta.get_field("recurrence").verbose_name,
        help_text=Aid._meta.get_field("recurrence").help_text,
    )
    subvention_rate_lower_bound = serializers.SerializerMethodField(
        "get_subvention_rate_lower_bound", label="Taux de subvention min (en %)"
    )
    subvention_rate_upper_bound = serializers.SerializerMethodField(
        "get_subvention_rate_upper_bound", label="Taux de subvention max (en %)"
    )

    def get_subvention_rate_lower_bound(self, obj):
        return getattr(obj.subvention_rate, "lower", None)

    def get_subvention_rate_upper_bound(self, obj):
        return getattr(obj.subvention_rate, "upper", None)

    class Meta:
        model = Aid


# First version of the API
class AidSerializer10(BaseAidSerializer):
    class Meta(BaseAidSerializer.Meta):
        fields = (
            "id",
            "slug",
            "url",
            "name",
            "short_title",
            "financers",
            "instructors",
            "description",
            "eligibility",
            "perimeter",
            "mobilization_steps",
            "origin_url",
            "application_url",
            "targeted_audiences",
            "aid_types",
            "destinations",
            "start_date",
            "predeposit_date",
            "submission_deadline",
            "subvention_rate_lower_bound",
            "subvention_rate_upper_bound",
            "contact",
            "recurrence",
            "project_examples",
            "date_created",
            "date_updated",
        )


# Add 'programs'
class AidSerializer11(BaseAidSerializer):
    class Meta(BaseAidSerializer.Meta):
        fields = (
            "id",
            "slug",
            "url",
            "name",
            "short_title",
            "financers",
            "instructors",
            "programs",
            "description",
            "eligibility",
            "perimeter",
            "mobilization_steps",
            "origin_url",
            "application_url",
            "targeted_audiences",
            "aid_types",
            "destinations",
            "start_date",
            "predeposit_date",
            "submission_deadline",
            "subvention_rate_lower_bound",
            "subvention_rate_upper_bound",
            "contact",
            "recurrence",
            "project_examples",
            "date_created",
            "date_updated",
        )


class CategoryRelatedField(serializers.StringRelatedField):
    def to_representation(self, value):
        return f"{value.theme}|{value}"


# Add 'categories'.
class AidSerializer12(BaseAidSerializer):

    categories = CategoryRelatedField(
        many=True,
        label="Thème et catégorie, séparés par « | ».",
        help_text='E.g: "Nature / environnement|Qualité de l\'air"',
    )

    class Meta(BaseAidSerializer.Meta):
        fields = (
            "id",
            "slug",
            "url",
            "name",
            "short_title",
            "financers",
            "instructors",
            "programs",
            "description",
            "eligibility",
            "perimeter",
            "mobilization_steps",
            "origin_url",
            "categories",
            "application_url",
            "targeted_audiences",
            "aid_types",
            "destinations",
            "start_date",
            "predeposit_date",
            "submission_deadline",
            "subvention_rate_lower_bound",
            "subvention_rate_upper_bound",
            "contact",
            "recurrence",
            "project_examples",
            "date_created",
            "date_updated",
        )


# Add 'loan_amount' and 'recoverable_advance_amount' fields.
# Remove 'tags'.
class AidSerializer13(BaseAidSerializer):

    categories = CategoryRelatedField(
        many=True,
        label="Thème et catégorie, séparés par « | ».",
        help_text='E.g: "Nature / environnement|Qualité de l\'air"',
    )

    class Meta(BaseAidSerializer.Meta):
        fields = (
            "id",
            "slug",
            "url",
            "name",
            "short_title",
            "financers",
            "instructors",
            "programs",
            "description",
            "eligibility",
            "perimeter",
            "mobilization_steps",
            "origin_url",
            "categories",
            "application_url",
            "targeted_audiences",
            "aid_types",
            "destinations",
            "start_date",
            "predeposit_date",
            "submission_deadline",
            "subvention_rate_lower_bound",
            "subvention_rate_upper_bound",
            "loan_amount",
            "recoverable_advance_amount",
            "contact",
            "recurrence",
            "project_examples",
            "date_created",
            "date_updated",
        )


# Add 'is_call_for_projects'.
class AidSerializer14(BaseAidSerializer):

    categories = CategoryRelatedField(
        many=True,
        label="Thème et catégorie, séparés par « | ».",
        help_text='E.g: "Nature / environnement|Qualité de l\'air"',
    )

    class Meta(BaseAidSerializer.Meta):
        fields = (
            "id",
            "slug",
            "url",
            "name",
            "short_title",
            "financers",
            "instructors",
            "programs",
            "description",
            "eligibility",
            "perimeter",
            "mobilization_steps",
            "origin_url",
            "categories",
            "is_call_for_project",
            "application_url",
            "targeted_audiences",
            "aid_types",
            "destinations",
            "start_date",
            "predeposit_date",
            "submission_deadline",
            "subvention_rate_lower_bound",
            "subvention_rate_upper_bound",
            "loan_amount",
            "recoverable_advance_amount",
            "contact",
            "recurrence",
            "project_examples",
            "date_created",
            "date_updated",
        )


# Add 'name_initial', 'import_data_url', 'import_data_mention' & 'import_share_licence'
class AidSerializer15(BaseAidSerializer):

    categories = CategoryRelatedField(
        many=True,
        label="Thème et catégorie, séparés par « | ».",
        help_text='E.g: "Nature / environnement|Qualité de l\'air"',
    )

    class Meta(BaseAidSerializer.Meta):
        fields = (
            "id",
            "slug",
            "url",
            "name",
            "name_initial",
            "short_title",
            "financers",
            "instructors",
            "programs",
            "description",
            "eligibility",
            "perimeter",
            "mobilization_steps",
            "origin_url",
            "categories",
            "is_call_for_project",
            "application_url",
            "targeted_audiences",
            "aid_types",
            "destinations",
            "start_date",
            "predeposit_date",
            "submission_deadline",
            "subvention_rate_lower_bound",
            "subvention_rate_upper_bound",
            "loan_amount",
            "recoverable_advance_amount",
            "contact",
            "recurrence",
            "project_examples",
            "import_data_url",
            "import_data_mention",
            "import_share_licence",
            "date_created",
            "date_updated",
        )


# Add 'is_charged' field
class AidSerializer16(BaseAidSerializer):

    categories = CategoryRelatedField(
        many=True,
        label="Thème et catégorie, séparés par « | ».",
        help_text='E.g: "Nature / environnement|Qualité de l’air"',
    )

    class Meta(BaseAidSerializer.Meta):
        fields = (
            "id",
            "slug",
            "url",
            "name",
            "name_initial",
            "short_title",
            "financers",
            "instructors",
            "programs",
            "description",
            "eligibility",
            "perimeter",
            "mobilization_steps",
            "origin_url",
            "categories",
            "is_call_for_project",
            "application_url",
            "targeted_audiences",
            "aid_types",
            "is_charged",
            "destinations",
            "start_date",
            "predeposit_date",
            "submission_deadline",
            "subvention_rate_lower_bound",
            "subvention_rate_upper_bound",
            "loan_amount",
            "recoverable_advance_amount",
            "contact",
            "recurrence",
            "project_examples",
            "import_data_url",
            "import_data_mention",
            "import_share_licence",
            "date_created",
            "date_updated",
        )


class AidSerializerLatest(AidSerializer16):
    pass


class AidAudienceSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    type = serializers.CharField()


class AidTypeSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    type = serializers.CharField()


class AidStepSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()


class AidRecurrenceSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()


class AidDestinationSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
