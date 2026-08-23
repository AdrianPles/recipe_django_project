from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_recipes, name='home'),
    path("create_recipe/", views.create_recipe, name='create_recipe'),
    path("delete_recipe/<int:pk>/", views.delete_recipe, name='delete_recipe'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)