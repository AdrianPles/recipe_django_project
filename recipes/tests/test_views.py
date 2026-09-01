import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse
from recipes.models import Recipe
User = get_user_model()


# decorator care creeaza bd provizorie pentru teste
# se creeaza un user in bd si se verifica
# verificam parola user-ului
@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        username="test1234",
        password="password1234"
    )
    assert user.username == "test1234"
    assert user.check_password("password1234")

# se creaza un user in bd
@pytest.fixture
def user(db) -> User:
    u = User.objects.create_user(
        username="test1234",
        password="password1234"
    )
    return u

# fixture
# functia creeaza un obiect pe care il putem folosi mai departe
# acest obiect se conecteaza la bd prin alt fixture db si client
@pytest.fixture
def logged_in_client(user, client: Client) -> Client:
    # se creeaza un browser simulat, logat, care poate face requesturi HTTP.
    client.login(
        username="test1234",
        password="password1234"
    )
    return client

# acest fixture ne creeaza o reteta pentru a putea fi folosita in teste
@pytest.fixture
def recipe(user):
    r = Recipe.objects.create(title="Tort cu fructe", description="citrice, frisca, blat", user=user)
    return r

def test_list_all_recipes(logged_in_client):
    # facem un HTTP GET request:
    response = logged_in_client.get("/")
    assert response.status_code == 200

def test_does_recipe_exist(logged_in_client, recipe):
    # facem un HTTP GET request:
    response = logged_in_client.get("/")
    assert response.status_code == 200
    assert "Tort cu fructe" in str(response.content)

def test_user_recipe_count(user):
    recipe1 = Recipe.objects.create(title="recipe1", description="ingrediente1", user=user)
    recipe2 = Recipe.objects.create(title="recipe2", description="ingrediente2", user=user)
    recipes = list(Recipe.objects.filter(user_id=user.pk))
    assert len(recipes) == 2

def test_user_recipe_count_html(user, client):
    recipe1 = Recipe.objects.create(title="recipe1", description="ingrediente1", user=user)
    recipe2 = Recipe.objects.create(title="recipe2", description="ingrediente2", user=user)
    recipe3 = Recipe.objects.create(title="recipe3", description="ingrediente3", user=user)
    response = client.get("/")
    assert response.status_code == 200
    main_page_text = str(response.content)
    assert main_page_text.count(f"/user/{user.pk}/recipes/") == 3

def test_delete_recipe(user, recipe, logged_in_client: Client):
    response = logged_in_client.post(f"/delete_recipe/{recipe.pk}/")
    assert response.status_code == 302
    # verificam daca s-a sters cartea din db
    response = logged_in_client.post(f"/delete_recipe/{recipe.pk}/")
    assert response.status_code == 404

def test_login_user_post_success(client, user):
    """Verifică dacă utilizatorul se poate loga cu succes cu date valide (POST)."""
    url = reverse("login")
    login_data = {
        "username": "test1234",
        "password": "password1234"
    }
    response = client.post(url, data=login_data)
    assert response.status_code == 302
    assert response.url == reverse("home")

def test_logout_user(logged_in_client: Client):
    url = reverse("logout")
    response = logged_in_client.get(url)
    assert response.status_code == 302
    assert response.url == reverse("home")

@pytest.mark.django_db
def test_register_user(client):
    url = reverse("register")
    register_data = {
        "username": "Aquamagic",
        "password1": "Altaparola1234!",
        "password2": "Altaparola1234!"
    }
    response = client.post(url, data=register_data)
    assert response.status_code == 302
    assert response.url == reverse("home")
    # verificam daca utilizatorul s-a salvat in db
    assert User.objects.filter(username="Aquamagic").exists() is True
