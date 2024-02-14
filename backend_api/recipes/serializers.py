from pprint import pprint

from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

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


    def update(self, instance, validated_data):
        if validated_data.get('steps'):
            steps_data = validated_data.pop('steps')
            for step_data in steps_data:
                step, created = Step.objects.get_or_create(order=step_data['order'], recipe=instance)

                for attr, value in step_data.items():
                    setattr(step, attr, value)
                step.save()

        tags = []
        if validated_data.get('tags'):
            tags_data = validated_data.pop('tags')

            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_data['name'])
                tags.append(tag)

        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        validated_data['tags'] = tags

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance