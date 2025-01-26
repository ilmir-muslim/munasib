from django.apps import AppConfig


class AdminsPanelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "admins_panel"

    def ready(self):
        import admins_panel.signals  # Подключаем файл с сигналами
