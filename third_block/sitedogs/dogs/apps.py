from django.apps import AppConfig


class DogsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dogs"

    def ready(self):
        import dogs.infrastructure.adapters.django_orm.orm  # type: ignore
