from pprint import pprint

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.utils import json

from .models import Recipe
from .serializers import FormDataSerializer, RecipeSerializer


class RecipeModelViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def create(self, request, *args, **kwargs):

        # валидация наличия json и файлов в форме
        serializer = FormDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        json_row = data.pop('json')

        if json_row:
            json_data = json.loads(json_row)
            data['name'] = json_data['name']
            data['description'] = json_data['description']
            data['ingredients'] = json_data['ingredients']
            data['cooking_instructions'] = json_data['cooking_instructions']
            data['cooking_time_in_minutes'] = json_data['cooking_time_in_minutes']

        data['image'] = data.pop('recipe_image')

        # валидация данных json строки (должны быть поля для модели Recipe)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # создание объекта в бд
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



    # @swagger_auto_schema(auto_schema=None)
    # def partial_update(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # def get_permissions(self):
    #     """Установка разных уровней доступа для методов"""
    #     if self.request.method == 'GET':
    #         permission_classes = [AllowAny]  # Метод GET доступен всем
    #     else:
    #         permission_classes = [IsAuthenticated]  # Остальные методы требуют авторизации
    #     return [permission() for permission in permission_classes]
    #
    # def perform_create(self, serializer):
    #     """Автоматически определяем user id и вставляем в соответствующее поле при создании рецепта"""
    #     serializer.save(user=self.request.user)
