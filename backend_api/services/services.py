import uuid

from django.core.exceptions import ValidationError


def generate_filename(instance, filename):
    """Функция для генерации имени файла на основе UUID."""
    extension = filename.split('.')[-1]  # получаем расширение файла
    filename = f'images/{uuid.uuid4().hex}.{extension}'  # создаем новое имя файла
    return filename


def validate_file_size(value):
    """Валидатор размера загружаемого изображения"""
    filesize = value.size

    if filesize > 2 * 1024 * 1024:
        raise ValidationError("Максимальный размер файла 2 МБ.")

def generate_filename_upload_photo(instance, filename)-> str:
    """Функция для генерации имени файла на основе UUID."""
    extension = filename.split('.')[-1]  # получаем расширение файла
    filename = f'foto/{uuid.uuid4().hex}.{extension}'  # создаем новое имя файла
    return filename