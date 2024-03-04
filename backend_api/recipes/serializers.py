from django.core import validators
from django.db import transaction
from django.http import HttpResponse, Http404
from rest_framework import serializers, fields
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from .models import Recipe, Step, Ingredient, RecipeIngredient, Measure


class FormDataSerializer(serializers.Serializer):
    json = fields.CharField()
    images = serializers.ListField(child=serializers.ImageField(
            max_length=(1024 * 1024 * 2),
            validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    ))

class IngredientSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        # Получаем оригинальное представление
        ret = super().to_representation(instance)

        # удаляем ключ 'name' и возвращаем только его значение
        return ret.pop('name')

    class Meta:
        model = Ingredient
        fields = ['name']


class MeasureSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        # Получаем оригинальное представление
        ret = super().to_representation(instance)

        # удаляем ключ 'name' и возвращаем только его значение
        return ret.pop('name')

    class Meta:
        model = Measure
        fields = ['name']


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['order', 'text', 'image', ]

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()
    measure = MeasureSerializer()

    def to_representation(self, instance):
        # Получаем оригинальное представление
        ret = super().to_representation(instance)
        # Переименовываем ключ 'ingredient' в 'name'
        if 'ingredient' in ret:
            ret['name'] = ret.pop('ingredient')

        # Возвращаем модифицированное представление
        return ret

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'amount', 'measure']


class RecipeSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True)

    def to_internal_value(self, data):
        ingredients = data.get("ingredients")
        for ingredient_data in ingredients:
            ingredient = ingredient_data.pop('name')
            ingredient_data['ingredient'] = {"name": ingredient}
            measure = ingredient_data.pop('measure')
            ingredient_data['measure'] = {"name": measure}

        return super().to_internal_value(data)


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
                  )

        read_only_fields = ('id', "published_at")

    @transaction.atomic
    def create(self, validated_data):
        steps_data = validated_data.pop('steps')
        ingredients_data = validated_data.pop('ingredients')

        # создаем рецепт
        recipe = super().create(validated_data)

        # создаем объекты 'step' в базе данных
        for step_data in steps_data:
            Step.objects.create(recipe=recipe, **step_data)

        for ingredient_data in ingredients_data:
            try:
                measure_name = ingredient_data.get("measure").get("name")
                measure = Measure.objects.get(name=measure_name)
            except Exception:
                raise ValidationError(f"Measure with name: '{measure_name}' does not exist")
            try:
                ingredient_name = ingredient_data.get("ingredient").get("name")
                ingredient = Ingredient.objects.get(name=ingredient_name)
            except Exception:
                raise ValidationError(f"Ingredient with name: '{ingredient_name}' does not exist")

            RecipeIngredient.objects.create(
                recipe=recipe,
                amount=ingredient_data.get('amount'),
                measure=measure,
                ingredient=ingredient
            )

        return recipe

    def update(self, instance, validated_data):
        if validated_data.get('steps'):
            steps_data = validated_data.pop('steps')
            for step_data in steps_data:
                step, created = Step.objects.get_or_create(order=step_data['order'], recipe=instance)

                for attr, value in step_data.items():
                    setattr(step, attr, value)
                step.save()

        instance = super().update(instance, validated_data)

        return instance
