from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

from django import template
import re

from django.contrib.auth.models import User



register = template.Library()

# Нужен для удаления картинок из превью статей
@register.filter
def remove_images(value):
    """Удаляет теги <img> из HTML-контента."""
    img_pattern = r'<img.*?>'
    return re.sub(img_pattern, '', value)

# Параметры категорий
class Category(models.Model):
    # Длинна имени категории максимум 100 символов
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Модель статей
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()  # текстовое поля расширеного функционала, позволяет ХРАНИТЬ в этом поле таблици БД форматированный текст и изображения (курсив, добавлять картинки, жирность текста и т.д.)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey('Category', related_name='posts', on_delete=models.CASCADE, default=1)  # default=1 указывает на первую категорию
    # Эти настройки помагли добавить изображение к превтю статьи (часть 3)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Поле для изображения

    # Возвращает краткий текст поста (выдержку) из первых num_words=50 слов
    def get_excerpt(self, num_words=50):
        words = self.content.split()[:num_words]
        if len(self.content.split()) > num_words:
            return remove_images(' '.join(words) + '...')
        return remove_images(' '.join(words))

    def __str__(self):
        return self.title


# Модель профиля пользователей
def profile_image_upload_path(instance, filename):
    return f'profile_images/user_{instance.user.id}/{filename}'


from django.core.exceptions import ValidationError

def validate_image_size(image):
    max_size = 3840 * 2160  # 4K в пикселях
    if image.file.size > max_size:
        raise ValidationError("Изображение превышает максимальный размер 4K.")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(
        # default='/blog/static/blog/images/default_profile.png',  # Путь относительно MEDIA_ROOT
        default='/../static/blog/images/default_profile.png',
        upload_to='profile_pics',  # Папка, куда будут загружаться изображения
        validators=[validate_image_size], 
        blank=True, 
        null=True, 
        help_text="Максимальное разрешение изображения: 4K"
    )

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'
    

