from rest_framework import serializers

from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):

    id = serializers.CharField(source='slug')
    text = serializers.CharField(source='name')

    class Meta:
        model = Project
        fields = ('id', 'text', 'status',)
