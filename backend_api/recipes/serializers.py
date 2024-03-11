from pprint import pprint

from django.core import validators
from django.db import transaction
from rest_framework import serializers, fields
from rest_framework.exceptions import ValidationError

from .models import Recipe, Step, Ingredient, RecipeIngredient, Measure


# ------------ FORM-DATA SERIALIZER ------------
class FormDataSerializer(serializers.Serializer):
    json = fields.JSONField()
    images = serializers.ListField(child=serializers.ImageField(
            max_length=(1024 * 1024 * 2),
            validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    ))

# ------------ INGREDIENT SERIALIZER ------------
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']

    def validate(self, data):
        try:
            ingredient_name = data.get("name")
            ingredient_obj = Ingredient.objects.get(name=ingredient_name)
            return ingredient_obj
        except Exception:
            raise ValidationError(f"Ingredient with name: '{ingredient_name}' does not exist")

    def to_representation(self, instance):
        # Получаем оригинальное представление
        ret = super().to_representation(instance)

        # удаляем ключ 'name' и возвращаем только его значение
        return ret.pop('name')


# ------------ MEASURE SERIALIZER ------------
class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ['name']

    def validate(self, data):
        try:
            measure_name = data.get("name")
            measure_obj = Measure.objects.get(name=measure_name)
            return measure_obj
        except Exception:
            raise ValidationError(f"Ingredient with name: '{measure_name}' does not exist")

    def to_representation(self, instance):
        # Получаем оригинальное представление
        ret = super().to_representation(instance)

        # удаляем ключ 'name' и возвращаем только его значение
        return ret.pop('name')


# ------------ STEP SERIALIZER ------------
class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['order', 'text', 'image', ]


# ------------ RECIPE INGREDIENT SERIALIZER ------------
class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'amount', 'measure']

    ingredient = IngredientSerializer()
    measure = MeasureSerializer()

    def to_internal_value(self, data):
        ingredient = data.pop('name')
        data['ingredient'] = {"name": ingredient}
        measure = data.pop('measure')
        data['measure'] = {"name": measure}
        super().to_internal_value(data)
        return data


# ------------ RECIPE SERIALIZER ------------
class RecipeSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True)

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

        recipe = super().create(validated_data)
        for step_data in steps_data:
            Step.objects.create(recipe=recipe, **step_data)

        for ingredient_data in ingredients_data:
            measure_name = ingredient_data.get("measure").get("name")
            measure = Measure.objects.get(name=measure_name)
            ingredient_name = ingredient_data.get("ingredient").get("name")
            ingredient = Ingredient.objects.get(name=ingredient_name)

            RecipeIngredient.objects.create(
                recipe=recipe,
                amount=ingredient_data.get('amount'),
                measure=measure,
                ingredient=ingredient
            )

        return recipe

    def update(self, instance: Recipe, validated_data):
        is_partial = self.partial

        if validated_data.get('steps'):
            steps_data = validated_data.pop('steps')
            for step_data in steps_data:
                step, created = Step.objects.get_or_create(order=step_data['order'], recipe=instance)

                for attr, value in step_data.items():
                    setattr(step, attr, value)
                step.save()

        if validated_data.get('ingredients'):
            ingredients_data = validated_data.pop('ingredients')

            # проверяем наличие в бд ингредиентов и единиц измерений. если все ок, подставляем объекты
            for ingredient_data in ingredients_data:
                try:
                    ingredient_name = ingredient_data.get("ingredient").get("name")
                    ingredient = Ingredient.objects.get(name=ingredient_name)
                    ingredient_data['ingredient'] = ingredient
                except Exception:
                    raise ValidationError(f"Ingredient with name: '{ingredient_name}' does not exist")

                if 'measure'in ingredient_data:
                    try:
                        measure_name = ingredient_data.get("measure").get("name")
                        measure = Measure.objects.get(name=measure_name)
                        ingredient_data['measure'] = measure
                    except Exception:
                        raise ValidationError(f"Measure with name: '{measure_name}' does not exist")

            # existed_ingredients_list = RecipeIngredient.objects.filter(recipe=instance)
            # new_ingredients_list = []
            #
            # for ingredient_data in ingredients_data:
            #     try:
            #         recipe_ingredient = RecipeIngredient.objects.get(ingredient=ingredient_data.get('ingredient'), recipe=instance)
            #         new_ingredients_list.append(recipe_ingredient)
            #         RecipeIngredient.objects.filter(
            #             ingredient=ingredient, recipe=instance).update(**ingredient_data)
            #     except Exception:
            #         RecipeIngredient.objects.create(
            #             recipe=instance,
            #             amount=ingredient_data.get('amount'),
            #             measure=ingredient_data.get('measure'),
            #             ingredient=ingredient_data.get("ingredient")
            #         )
            #
            # print(new_ingredients_list)
            # print(existed_ingredients_list)


            # if not is_partial:
            #     instance.ingredients.set([])
            #     instance.save()
            #     pprint(instance.ingredients)
            # for ingredient_data in ingredients_data:
            #     recipe_ingredient = RecipeIngredient.objects.get(ingredient=ingredient, recipe=instance)
            #     if recipe_ingredient:
            #         RecipeIngredient.objects.filter(
            #             ingredient=ingredient, recipe=instance).update(**ingredient_data)

        instance = super().update(instance, validated_data)
        return instance



"""
            # Получаем текущие объекты ingredients
            current_recipe_ingredients = {recipe_ingredient.id: recipe_ingredient for recipe_ingredient in instance.ingredients.all()}

            # Обрабатываем новые данные
            for recipe_ingredient_data in ingredients_data:
                recipe_ingredient_id = recipe_ingredient_data.get('id')
                if recipe_ingredient_id:
                    # Обновляем существующий объект
                    current_recipe_ingredients.pop(recipe_ingredient_id, None)
                    recipe_ingredient = instance.ingredients.filter(id=recipe_ingredient_id).first()
                    if recipe_ingredient:
                        # Здесь обновляем данные ingredient на основе recipe_ingredient_data
                        recipe_ingredient.update(**recipe_ingredient_data)
                else:
                    # Создаем новый объект
                    RecipeIngredient.objects.create(**recipe_ingredient_data, recipe=instance)
            
            if not is_partial:
                # Удаляем несуществующие объекты
                for recipe_ingredient in current_recipe_ingredients.values():
                    recipe_ingredient.delete()
                    
Сначала получите текущий набор объектов ingredients, связанных с основным объектом.
Создайте словарь, где ключами будут уникальные идентификаторы (ID) текущих объектов ingredients.
Обработайте новые данные, переданные в запросе обновления. Для каждого нового объекта ingredient проверьте, 
существует ли он уже в текущем наборе. Если объект существует, обновите его данные. 
Если нет, создайте новый объект.
После обработки всех новых данных, переберите словарь текущих объектов ingredients. 
Если какой-либо объект не был обновлен или создан в новом наборе данных, удалите его.
"""


