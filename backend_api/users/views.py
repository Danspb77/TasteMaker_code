from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .models import User
from .serializers import RegistrationSerializer, UserUpdateSerializer, UserSerializer


@extend_schema_view(
    post=extend_schema(summary='Регистрация пользователя', tags=['Аутентификация & Авторизация']),
    get=extend_schema(summary='Получение данных пользователя', tags=['Аутентификация & Авторизация'])
)
class UserCreateView(generics.CreateAPIView):
    """Оправляет POST запрос для регистрации пользователя в БД"""
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Создать пользователя могут не авторизированные пользователи



    def post(self, request, *args, **kwargs):
        """Метод возвращает статус POST запроса"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED)

@extend_schema_view(
    get=extend_schema(summary='Получение данных пользователя', tags=['Аутентификация & Авторизация']),
    patch=extend_schema(summary='Частичное редактирование данных пользователя', tags=['Аутентификация & Авторизация']),
    put=extend_schema(summary='Полное редактирование данных пользователя', tags=['Аутентификация & Авторизация'])
)
class UserRUDView(generics.RetrieveUpdateAPIView):
    """Представление модели Пользователя"""
    queryset = User.objects.all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(status=status.HTTP_201_CREATED)

