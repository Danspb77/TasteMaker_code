# Generated by Django 5.0.1 on 2024-01-29 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_recipe_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='user_id',
        ),
    ]
