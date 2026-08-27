from django.db.models import Model
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from .models import Recipe
from django.db.models.functions import Lower


def home(request: HttpRequest):
    return HttpResponse("Welcome to my webserver!")

def list_recipes(request: HttpRequest):
    # am declarat variabilele 'category_filter', 'by' si 'sort' pentru a realiza doua label-uri de filtrare/sortare, iar 'query' este variabila care se ocupa de cautarea cuvantului cheie din casuta de cautare.
    query = request.GET.get("q")
    category_filter = request.GET.get("category", "all")
    by = request.GET.get("by", "title")
    sort = request.GET.get("sort", "asc")
    recipes = Recipe.objects.all()
    # __icontains caută cuvântul oriunde în titlu și ignoră literele mari/mici
    if query:
        recipes = recipes.filter(title__icontains=query)
    # logica ne permite afisarea unei singure categorii selectate de utilizator
    if category_filter != "all":
        recipes = recipes.filter(category=category_filter)
    # pentru o sortare corecta dupa 'titlu reteta' folosim functia Django/Lower
    if by == "title":
        if sort == "asc":
            recipes = recipes.order_by(Lower("title"))
        else:
            recipes = recipes.order_by(Lower("title").desc())
    else:
        criterii_sortare = {
            "category": "category",
            "created_at": "created_at"
        }
        camp_baza_de_date = criterii_sortare.get(by, "title")
        if sort == "desc":
            camp_baza_de_date = f"-{camp_baza_de_date}"
        recipes = recipes.order_by(camp_baza_de_date)
    return render(request, "recipes/home.html", context={"recipes": recipes})

def list_user_recipes(request: HttpRequest, user_pk: int):
    query = request.GET.get("q")
    category_filter = request.GET.get("category", "all")
    by = request.GET.get("by", "title")
    sort = request.GET.get("sort", "asc")
    recipes = Recipe.objects.filter(user_id= user_pk)
    # __icontains caută cuvântul oriunde în titlu și ignoră literele mari/mici
    if query:
        recipes = recipes.filter(title__icontains=query)
    # logica ne permite afisarea unei singure categorii selectate de utilizator
    if category_filter != "all":
        recipes = recipes.filter(category=category_filter)
    # pentru o sortare corecta dupa 'titlu reteta' folosim functia Django/Lower
    if by == "title":
        if sort == "asc":
            recipes = recipes.order_by(Lower("title"))
        else:
            recipes = recipes.order_by(Lower("title").desc())
    else:
        criterii_sortare = {
            "category": "category",
            "created_at": "created_at"
        }
        camp_baza_de_date = criterii_sortare.get(by, "title")
        if sort == "desc":
            camp_baza_de_date = f"-{camp_baza_de_date}"
        recipes = recipes.order_by(camp_baza_de_date)
    return render(request, "recipes/home.html", context={"recipes": recipes})

@login_required()
def create_recipe(request: HttpRequest):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # aici cream o reteta in db
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect("home")
    else:
        form = RecipeForm()
        return render(request, "recipes/recipe_form.html", context={"form": form})

@login_required()
def delete_recipe(request: HttpRequest, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user.pk == recipe.user.pk:
        if request.method == "POST":
            recipe.delete()
            return redirect("home")
        else:
            return render(request, "recipes/recipe_confirm_delete.html", context={"recipe": recipe})
    else:
        return HttpResponse("Nu ai permisiunea de a șterge rețeta altui utilizator!")

def update_recipe(request: HttpRequest, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        recipe_instance = RecipeForm(request.POST, request.FILES, instance=recipe)
        if recipe_instance.is_valid():
            recipe_instance.save()
            return redirect("home")
    else:
        form = RecipeForm(instance=recipe)
        return render(request, "recipes/update_recipe_form.html", context={"form": form})
