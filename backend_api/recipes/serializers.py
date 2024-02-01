from rest_framework import serializers
from .models import Category, Recipe

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class RecipeSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=True)
    class Meta:
        model = Recipe
        fields = '__all__'
        # read_only_fields = ('user',)

    # def create(self, validated_data):
    #     categories_data = validated_data.pop('category')
    #     recipe = Recipe.objects.create(**validated_data)
    #
    #     for category_data in categories_data:
    #         category_name = category_data.get('name')
    #         category, created = Category.objects.get_or_create(name=category_name)
    #         recipe.category.add(category)
    #
    #     return recipe
    #
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['category'] = [category.name for category in instance.category.all()]
    #     return representation
