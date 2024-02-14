from rest_framework import serializers

from .models import Recipe, Step, Tag


class FormDataSerializer(serializers.Serializer):
    json = serializers.CharField(max_length=2000)
    recipe_image = serializers.ImageField(max_length=(1024 * 1024 * 2))
    step1_image = serializers.ImageField(max_length=(1024 * 1024 * 2), required=False)
    step2_image = serializers.ImageField(max_length=(1024 * 1024 * 2), required=False)
    step3_image = serializers.ImageField(max_length=(1024 * 1024 * 2), required=False)
    step4_image = serializers.ImageField(max_length=(1024 * 1024 * 2), required=False)
    step5_image = serializers.ImageField(max_length=(1024 * 1024 * 2), required=False)
    step6_image = serializers.ImageField(max_length=(1024 * 1024 * 2), required=False)
    step7_image = serializers.ImageField(max_length=(1024 * 1024 * 2), required=False)
    step8_image = serializers.ImageField(max_length=(1024 * 1024 * 2), required=False)
    step9_image = serializers.ImageField(max_length=(1024 * 1024 * 2), required=False)
    step10_image = serializers.ImageField(max_length=(1024 * 1024 * 2), required=False)


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['order', 'text', 'image',]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name',]


class RecipeSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id',
                  "name",
                  'description',
                  'ingredients',
                  'image',
                  'cooking_instructions',
                  'cooking_time',
                  'steps',
                  'tags',
                  )

        read_only_fields = ('id', "published_at")


    def create(self, validated_data):
        steps_data = validated_data.pop('steps')

        # создаем 'tag', если не существует
        tags_data = validated_data.pop('tags')
        tags = []
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            tags.append(tag)

        # создаем рецепт
        recipe = Recipe.objects.create(**validated_data)
        # устанавливаем теги
        recipe.tags.set(tags)

        # создаем объекты 'step' в базе данных
        for step_data in steps_data:
            Step.objects.create(recipe=recipe, **step_data)

        return recipe

    """
    # список категорий, принятый сервером
    category = serializers.ListField(write_only=True)
    # список категорий в ответе сервера
    category_data = serializers.SerializerMethodField()

    def validate(self, attrs):
        request = self.context.get('request')
        if request:
            # получаем список категорий в виде строки и превращаем в список
            categories_data_str = attrs.get('category')
            categories_data = [name.strip() for name in categories_data_str[0].split(",")]

            # ищем объекты 'category' по имени и складываем в список, создаем если не найдено
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
    """


"""
from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError
from django.core.files.uploadedfile import TemporaryUploadedFile

class FormDataParser(BaseParser):

    # Парсер для обработки form-data в Django DRF


    media_type = 'multipart/form-data'

    def parse(self, stream, media_type=None, parser_context=None):
        try:
            import requests
        except ImportError:
            raise ImportError("Необходима установка библиотеки 'requests' для работы с формами")

        # Извлечение данных запроса из контекста
        request = parser_context['request']

        # Получение данных form-data
        data = request.POST.dict()
        files = request.FILES

        # Обработка форм файлов
        form_files = {}
        for key, file in files.items():
            if isinstance(file, TemporaryUploadedFile):
                # Если файл уже является экземпляром TemporaryUploadedFile, добавляем его в словарь
                form_files[key] = file
            else:
                # Если файл еще не был сохранен на сервере, сохраняем его временно
                temp_file = TemporaryUploadedFile(file.name, file.content_type, file.size, file.charset)
                temp_file.write(file.read())
                temp_file.seek(0)
                form_files[key] = temp_file

        return data, form_files

"""
