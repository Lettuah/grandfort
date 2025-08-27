from django.apps import AppConfig


class ExpenditureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.expenditure'


    def ready(self):
        import apps.expenditure.signals
