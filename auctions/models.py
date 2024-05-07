from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("AuctionListing", blank=True, related_name="watched_by")

    def __str__(self):
        return self.username
    
    def is_watching(self, listing):
        return self.watchlist.contains(listing)


class AuctionCategory(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    category = models.ForeignKey(AuctionCategory, on_delete=models.CASCADE, related_name="items")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    price = models.FloatField()
    photo = models.URLField(max_length=256, blank=True)
    description = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    @property
    def pretty_price(self):
        return f"${self.price:,.2f}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField()

    def __str__(self):
        return f"Bid for {self.auction_listing}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    date = models.DateField()
    text = models.CharField(max_length=256)

    def __str__(self):
        return f"Comment on {self.auction_listing}"
