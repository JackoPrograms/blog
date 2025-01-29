from django.contrib import admin
from .models import Post, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget  # Необходим для загрузки файлов в приложение в папку с media
from django import forms

class PostAdminForm(forms.ModelForm):  # Определяет форму PostAdminForm для модели Post.
    content = forms.CharField(widget=CKEditorUploadingWidget())  # Заменяет стандартный текстовый виджет на CKEditorWidget для поля content. По сути добавляет редактор текста с возможностью, выделения, подчёркивани, курсивом, вставки изображений, таблиц и т.д.

    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):  #  класс PostAdmin, который представляет настройки административного интерфейса для модели Post.
    form = PostAdminForm
    list_display = ('title', 'created_at', 'updated_at', 'category')  # При отображении в панели админестратора
    fields = ('title', 'content', 'category', 'image')  # При редоктировании в панели админестратора

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
