from rest_framework import serializers

from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='name')
    text = serializers.CharField(source='name')

    class Meta:
        model = Tag
        fields = ('id', 'text')
