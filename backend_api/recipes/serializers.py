from rest_framework import serializers, fields
from rest_framework.exceptions import ValidationError

from .models import Recipe, Step, Ingredient


class IngredientSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):

        # Получаем оригинальное представление
        ret = super().to_representation(instance)

        # удаляем ключ 'name' и возвращаем только его значение
        return ret.pop('name')

    class Meta:
        model = Ingredient
        fields = ['name']


def validate_image(value):
    if not value.name.endswith(('.jpg', '.png', '.jpeg')):
        raise ValidationError("Only JPG, JPEG, PNG files are allowed.")

class FormDataSerializer(serializers.Serializer):
    json = fields.CharField()
    images = serializers.ListField(child=serializers.ImageField(
        max_length=(1024 * 1024 * 2),
        validators=[validate_image]))

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['order', 'text', 'image',]


class RecipeSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)

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


    def create(self, validated_data):
        steps_data = validated_data.pop('steps')

        # создаем рецепт
        recipe = super().create(validated_data)

        # создаем объекты 'step' в базе данных
        for step_data in steps_data:
            Step.objects.create(recipe=recipe, **step_data)

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