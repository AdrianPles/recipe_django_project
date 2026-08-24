from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipeForm
from .models import Recipe

def home(request: HttpRequest):
    return HttpResponse("Welcome to my webserver!")

def list_recipes(request: HttpRequest):
    recipes = Recipe.objects.all()
    return render(request, "recipes/home.html", context={"recipes": recipes})

def create_recipe(request: HttpRequest):
    if request.method == "POST":
        recipe_instance = RecipeForm(request.POST)
        if recipe_instance.is_valid():
            # aici cream o reteta in db
            recipe_instance.save()
            return redirect("home")
    else:
        form = RecipeForm()
        return render(request, "recipes/recipe_form.html", context={"form": form})

def delete_recipe(request: HttpRequest, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        recipe.delete()
        return redirect("home")
    else:
        return render(request, "recipes/recipe_confirm_delete.html", context={"recipe": recipe})

def update_recipe(request: HttpRequest, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        recipe_instance = RecipeForm(request.POST, instance=recipe)
        if recipe_instance.is_valid():
            recipe_instance.save()
            return redirect("home")
    else:
        form = RecipeForm(instance=recipe)
        return render(request, "recipes/update_recipe_form.html", context={"form": form})
