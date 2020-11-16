from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .static.auctions.utils import CATEGORIES
from .models import User, Bid, Listing, Comment


def index(request):
    active_listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": active_listings
    })


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
    winning_bid = False
    user = request.user

    #getting the listing the user clicked on
    get_listing = Listing.objects.filter(pk=listing_id)

    #user who is viewing the site
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)

        try:
            is_owner = bool(Listing.objects.get(owner=user, pk=get_listing[0].pk))
        except Listing.DoesNotExist:
            is_owner = False
        
        if request.method == "POST":

            #Bid code
            if 'bid' in request.POST:

                if request.POST.get('bid') == "":
                    messages.add_message(request, messages.WARNING, 'Please, place a bet.', extra_tags='alert-warning')
                    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))

                bid = float(request.POST.get('bid'))   

                if place_bid(bid, user, get_listing) == True:
                    #alert the user with a success message
                    messages.add_message(request, messages.SUCCESS, 'Bid was placed Successfully!', extra_tags='alert-success')
                    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))
                else:
                    messages.add_message(request, messages.ERROR, 'Bid must be higher than current ask price. Try again.', extra_tags='alert-danger')
                    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))

    return render(request, "auctions/listing.html", {
        "listing": get_listing[0]
    })

def place_bid(bid, user, listing_number):
    get_listing = Listing.objects.get(pk=listing_number[0].pk)
    #change starting_bid variable to a better name6
    if bid > get_listing.starting_bid:
        bid_contender = Bid()
        bid_contender.user = user
        bid_contender.bid = bid
        bid_contender.listing = get_listing
        bid_contender.save()

        get_listing.starting_bid = bid
        get_listing.save()
        return True
    else:
        return False


    

    
