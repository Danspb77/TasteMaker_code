from rest_framework import serializers
from .models import Category, Recipe



class RecipeSerializer(serializers.ModelSerializer):
    category = serializers.ListField(write_only=True)
    category_data = serializers.SerializerMethodField()

    def validate(self, attrs):
        request = self.context.get('request')
        if request:
            categories_data = attrs.get('category')

            categories = []
            for category_name in categories_data:
                category, created = Category.objects.get_or_create(name=category_name)
                categories.append(category)

            attrs['category'] = categories
            return attrs

    def get_category_data(self, instance):
        return instance.category.values_list('name', flat=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category_data'] = self.get_category_data(instance)
        return representation

    class Meta:
        model = Recipe
        fields = "__all__"
        read_only_fields = ('user', "category_data")


