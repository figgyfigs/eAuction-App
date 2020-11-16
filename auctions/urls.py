from django.urls import path
from django.contrib.auth import views as auth

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("create_listing", views.create, name="create_listing"),
    path("all_listings", views.all_listings, name="all_listings"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
]
