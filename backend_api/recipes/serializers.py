from rest_framework import serializers
from .models import Recipe, Category


class CategoryListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        return [item.name for item in data]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
        list_serializer_class = CategoryListSerializer

class RecipeSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    class Meta:
        model = Recipe
        fields = '__all__'
        #read_only_fields = ('user',) #включить при активном запросе токена на эндпойнт recipe
