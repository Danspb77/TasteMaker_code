from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RecipeModelViewSet

router = DefaultRouter()
router.register(prefix='', viewset=RecipeModelViewSet, basename='recipe-model')

urlpatterns = [
    path('/', include(router.urls)),
]


path('recipes/<int:pk>/', views.RecipeModelViewSet.as_view({'get': 'list'}), name='recipes-details'),
