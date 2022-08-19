from rest_framework import serializers

from keywords.models import SynonymList


class SynonymListSerializer(serializers.ModelSerializer):
    """
    Pourquoi renommer 'name' en 'text' ? Pour l'autocomplete avec select2.
    """

    id = serializers.CharField(source='keywords_list')
    text = serializers.CharField(source='autocomplete_name')
    name = serializers.CharField()

    class Meta:
        model = SynonymList
        fields = ('id', 'text', 'name')
