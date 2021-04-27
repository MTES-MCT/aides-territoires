from rest_framework import serializers

from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):

    text = serializers.CharField(source='name')

    class Meta:
        model = Project
        fields = ('slug', 'text', 'key_words', 'status',)
