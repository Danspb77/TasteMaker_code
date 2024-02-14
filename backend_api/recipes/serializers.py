from rest_framework import serializers

from .models import Recipe


class FormDataSerializer(serializers.Serializer):
    json = serializers.CharField(max_length=200)
    recipe_image = serializers.ImageField(max_length=(1024 * 1024 * 2))


# upload_to - задает путь, куда будут сохраняться загруженные изображения.
# null - указывает, может ли поле быть пустым (True/False).
# blank - указывает, является ли поле обязательным для заполнения в форме (True/False).
# max_length - задает максимальную длину имени файла (по умолчанию - 100).
# height_field - указывает имя поля, которое будет содержать высоту изображения.
# width_field - указывает имя поля, которое будет содержать ширину изображения.
# validators - позволяет определить список валидаторов для проверки загружаемого изображения.
# help_text - определяет текст справки, отображаемый при использовании формы или API.
# default - задает значение по умолчанию для поля.
# editable - указывает, может ли поле редактироваться пользователем (True/False).


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id',
                  "name",
                  'description',
                  'ingredients',
                  'image',
                  'cooking_instructions',
                  'cooking_time_in_minutes',
                  # 'category',
                  # 'category_data',
                  )

        read_only_fields = ('id', "category_data", "published_at")

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
