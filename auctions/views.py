from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .models import User


def index(request):
    return render(request, "auctions/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "POST":
        item = Listing()
        item.owner = User.objects.get(username=request.user)
        item.title = request.POST["title"]
        item.description = request.POST["description"]
        item.starting_bid = request.POST["starting_bid"]
        item.category = request.POST["category"]
        item.image_url = request.POST["url"]
        item.active = True
        item.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html", {"categories": CATEGORIES})

@login_required(login_url="/login")
def all_listings(request):
    all_products = Listing.objects.all()
    empty = False
    if len(all_products) == 0:
        empty = True
    
    return render(request, "auctions/all_listings.html", {
        "all_products": all_products,
        "empty": empty
    })

    
def listing(request, listing_id):
    on_watchlist = False
    is_owner = False
    user = request.user

    #get_listing == listing the user clicked on
    get_listing = Listing.objects.filter(pk=listing_id)

    #user who is viewing the site
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
    else:
        user = False

    return render(request, "auctions/listing.html", {
        "listing": get_listing[0]
    })

