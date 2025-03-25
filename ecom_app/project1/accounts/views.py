from django.contrib.auth.models import User
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Product
import requests
import random


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["contact"]  
        password1 = request.POST["password1"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect("login")  

    return render(request, "register.html")                       

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Log in successful! Redirecting...")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  

    return render(request, "login.html") 

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def store(request):
    products = Product.objects.all()  
    random_products = list(products)  
    random.shuffle(random_products)  
    random_products = random_products[:5]  

    context = {
        'products': products,
        'random_products': random_products,  
    }
    return render(request, 'store.html', context)

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


API_URL = "https://www.freetogame.com/api/games"
HEADERS = {
    "x-rapidapi-key": "051f45ddb8msh149b75ee4e86b83p1e4ffbjsn5e6bd5ef6067",
    "x-rapidapi-host": "free-to-play-games-database.p.rapidapi.com"
}

@login_required
def games(request):
    search_query = request.GET.get('search', '')
    selected_tags = request.GET.getlist('tags')  # Get selected categories

    # Define available tags based on FreeToGame API
    available_tags = [
        "mmorpg", "shooter", "strategy", "moba", "racing", "sports", "social", "sandbox",
        "open-world", "survival", "pvp", "pve", "pixel", "voxel", "zombie", "turn-based",
        "first-person", "third-person", "top-down", "tank", "space", "sailing", "side-scroller",
        "superhero", "permadeath", "card", "battle-royale", "mmo", "mmofps", "mmotps", "3d",
        "2d", "anime", "fantasy", "sci-fi", "fighting", "action-rpg", "action", "military",
        "martial-arts", "flight", "low-spec", "tower-defense", "horror", "mmorts"
    ]

    # Base URL for fetching games
    url = API_URL

    # If category is selected, modify the API request URL
    if selected_tags:
        url = f"{API_URL}?category={','.join(selected_tags)}"

    # Fetch game data
    response = requests.get(url)
    games = response.json() if response.status_code == 200 else []

    # Filter games by search query
    if search_query:
        games = [game for game in games if search_query.lower() in game["title"].lower()]

    return render(request, "freegames.html", {
        "games": games,
        "selected_tags": selected_tags,
        "available_tags": available_tags,
    })

@login_required
def game_detail(request, game_id):
    # Fetch game data from the FreeToGame API using the correct URL format
    url = f"https://www.freetogame.com/api/game?id={game_id}"
    response = requests.get(url)

    if response.status_code == 200:
        game = response.json()
    else:
        game = None  # Handle the case where the game is not found
    
    return render(request, "game_detail.html", {'game': game})
@login_required
def faq_view(request):
    return render(request, 'faqs.html')
@login_required
def news_view(request):
    return render(request, 'news.html')

def logout_view(request):
    logout(request)
    return redirect('index')


