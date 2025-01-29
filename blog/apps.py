from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    # Свяжим сигнал с приложением. Это было нужно для работы сигнала в (signals.py) который автоматизирует создание пользователей в Django, т.е. их не нужно создавать вручную.
    def ready(self):
        import blog.signals

