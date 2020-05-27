from django.apps import AppConfig


class KryptoniteConfig(AppConfig):
    name = 'kryptonite'

    def ready(self):
        from kryptonite.scheduler import logupdater
        logupdater.start()
