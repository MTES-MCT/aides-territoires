from rest_framework import serializers

from backers.models import Backer


class BackerSerializer(serializers.ModelSerializer):
    """
    Pourquoi renommer 'name' en 'text' ? Pour l'autocomplete avec select2.
    """

    id = serializers.CharField(source='id_slug')
    text = serializers.CharField(source='name')
    perimeter = serializers.StringRelatedField()

    class Meta:
        model = Backer
        fields = ('id', 'text', 'perimeter')
