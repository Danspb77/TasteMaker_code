from datetime import timedelta

from django.core import validators
from django.db import models

from .utils import generate_filename, validate_file_size
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # при удалении данного юзера, удалятся все, связанные с ним рецепты.
    description = models.TextField(max_length=1500)
    image = models.ImageField(upload_to=generate_filename,
                              validators=[
                                  validators.FileExtensionValidator(['png', 'jpg', 'jpeg']),
                                  validate_file_size])
    ingredients = models.TextField(max_length=1500)
    cooking_instructions = models.TextField(max_length=1500)
    cooking_time = models.DurationField(default=timedelta(minutes=0))
    published_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Step(models.Model):
    order = models.IntegerField()
    text = models.CharField(max_length=150)
    image = models.ImageField(null=True,
                              upload_to=generate_filename,
                              validators=[
                                  validators.FileExtensionValidator(['png', 'jpg', 'jpeg']),
                                  validate_file_size])
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['recipe', 'order']
        ordering = ['order']

    def __str__(self):
        return '%d: %s: %s' % (self.order, self.text, self.image.name)
