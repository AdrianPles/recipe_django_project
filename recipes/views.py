from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
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
            return redirect("create_recipe")
    else:
        form = RecipeForm()
        return render(request, "recipes/recipe_form.html", context={"form": form})