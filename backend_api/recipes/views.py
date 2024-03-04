from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from .models import Recipe, Ingredient, Measure
from .serializers import FormDataSerializer, RecipeSerializer, IngredientSerializer, MeasureSerializer


class IngredientModelView(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class MeasureModelView(generics.ListAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer

class RecipeModelViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def find_image_file(self, value, images):
        for file in images:
            if str(file) == value:
                return file

    def replace_filenames_with_files(self, data, images):
        for key, value in data.items():
            if key == 'image':
                data[key] = self.find_image_file(value, images)
            elif isinstance(value, dict):
                self.replace_filenames_with_files(value, images)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self.replace_filenames_with_files(item, images)
        return data


    def create(self, request, *args, **kwargs):

        serializer = FormDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        images = data.pop('images')
        data = data.pop('json')

        data = self.replace_filenames_with_files(data, images)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        serializer = FormDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        images = data.pop('images')
        data = data.pop('json')

        data = self.replace_filenames_with_files(data, images)

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


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
