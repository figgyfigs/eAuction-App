from django.contrib.auth.models import AbstractUser
from django.db import models

from .static.auctions.utils import CATEGORIES


class User(AbstractUser):
    pass

class Listing(models.Model):
    owner = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=15, choices=CATEGORIES)
    image_url = models.URLField(max_length=200)
    active = models.BooleanField(default=True)

class Bid(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=150)

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ManyToManyField(Listing, blank=True)

