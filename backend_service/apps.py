from django.apps import AppConfig


class BackendServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend_service'

    def ready(self):

        from django.contrib.auth.models import User
        from rest_framework.authtoken.models import Token

        try:
            for user in User.objects.all():
                Token.objects.get_or_create(user=user)
        except Exception:
            pass
