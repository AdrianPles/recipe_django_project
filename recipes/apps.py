from django.apps import AppConfig


class RecipesConfig(AppConfig):
    name = 'recipes'

    def ready(self):
        # observer
        import recipes.signals
