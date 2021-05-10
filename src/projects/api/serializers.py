from rest_framework import serializers

from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):

    '''
    We add 'id' and 'text' fields to use Select2
    for the autocomplete input field in step project
    '''

    id = serializers.CharField(source='id_slug')
    text = serializers.CharField(source='name')

    class Meta:
        model = Project
        fields = ('id', 'text', 'key_words', 'status',)
