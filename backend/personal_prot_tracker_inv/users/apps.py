from django.apps import AppConfig

 # Import the users module to ensure signals are loaded
#  To make the signal work, we need to import it when the app is ready.


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'users'

    def ready(self):
        import users.signals

# Although the signal is in models.py, this is a clean way to ensure it's loaded. Let's create that file for convention.

