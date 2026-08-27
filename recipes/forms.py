from django import forms
from . models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "category", "cooking_time", "imagine_prezentare"]
        # Am adăugat widgets în clasa Meta. Am mapat câmpul description la un element HTML de tip Textarea.
        # Am folosit attrs pentru a injecta cod HTML, unde placeholder este textul care va apărea șters (gri) în interiorul căsuței până când utilizatorul începe să scrie.
        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Exemplu:\n- 200g făină\n- 2 ouă\n\nPași:\n1. Se amestecă ingredientele...',
                'rows': 15,
            }),
        }