from rest_framework import serializers

from categories.models import Theme, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'slug', 'name')


class ThemeSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True)

    class Meta:
        model = Theme
        fields = ('id', 'slug', 'name', 'categories')
