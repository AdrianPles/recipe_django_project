from django.db import models
from django.db.models.fields import DateTimeField
from django.contrib.auth import get_user_model

User = get_user_model()

class Recipe(models.Model):
    class Meta:
        # în limba română cu diacritice, configurăm afișarea la singular și plural în interfețe (ex: Django Admin).
        verbose_name = 'Rețetă'
        verbose_name_plural = 'Rețete'
    # definim un atribut al clasei Recipe, acesta fiind o lista fixa de tupluri, reprezentand optiunile din care utilizatorul poate selecta, cand alege categoria din care face parte reteta (primul elem. afisare in db/al doile elm. afisare pt. user)

    CATEGORY_CHOICES = [
        ('mic_dejun', 'Mic dejun'),
        ('ciorbe', 'Ciorbe / Supe'),
        ('fel_principal', 'Fel principal'),
        ('desert', 'Desert'),
        ('patiserie', 'Patiserie'),
        ('panificatie', 'Panificație')
    ]
        # verbose=name -> un parametru predefinit din Django programat sa caute exact acest nume in cod, petru a sti ce text sa afiseze pe ecran
        # django ORM (Object-Relational Mapping) legatura dintre db si cod
    title = models.CharField(
        max_length=150,
        verbose_name='Titlu rețetă'
    )
    description = models.TextField(
        verbose_name='Descriere și pași preparare',
        help_text='Scrie aici ingredientele și modul de preparare al rețetei.'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Fel principal',
        verbose_name='Categorie'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Dată creare'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Timp de gătire (minute)',
        help_text='Introdu timpul total exprimat în minute.',
        default=30
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='recipes')
    imagine_prezentare = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return self.title


