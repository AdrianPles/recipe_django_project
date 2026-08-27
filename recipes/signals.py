from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Recipe

@receiver(post_delete, sender=Recipe)
def delete_imagine_prezentare_on_recipe_delete(sender, instance: Recipe, **kwargs):
    if instance.imagine_prezentare:
        instance.imagine_prezentare.delete(save=False)

@receiver(pre_save, sender=Recipe)
def delete_imagine_prezentare_on_update(sender, instance: Recipe, **kwargs):
    if not instance.pk:
        # daca reteta nu exista inca in bd.
        return
    try:
        old_recipe = Recipe.objects.get(pk=instance.pk)
        if old_recipe.imagine_prezentare and old_recipe.imagine_prezentare.name != instance.imagine_prezentare.name:
            old_recipe.imagine_prezentare.delete(save=False)
    except Recipe.DoesNotExist:
        return
    