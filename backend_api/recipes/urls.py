from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RecipeModelViewSet, IngredientModelView

router = DefaultRouter()
router.register(prefix='', viewset=RecipeModelViewSet, basename='recipe-model')

urlpatterns = [
    path('', include(router.urls)),
    path('ingredients', IngredientModelView.as_view(), name='ingredients'),
]