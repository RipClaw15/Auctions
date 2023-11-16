from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


    
class Listing(models.Model):
    
    VEHICLES = "Vehicles"
    PROPERTIES = "Properties"
    CLOTHES = "Clothes"
    ELECTRONICS = "Electronics"
    ANIMALS = "Animals"
    SPORTS = "Sports"
    OTHERS = "Others"

    CATEGORY = [
        (VEHICLES, "Vehicles"),
        (PROPERTIES, "Properties"),
        (CLOTHES, "Clothes"),
        (ELECTRONICS, "Electronics"),
        (ANIMALS, "Animals"),
        (SPORTS, "Sports"),
        (OTHERS, "Others"),
    ]
    
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    description = models.CharField(max_length=150)
    category = models.CharField(max_length=16, choices=CATEGORY, default=VEHICLES)
    image_url = models.URLField(blank=True)
    listed_on = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank = True, null = True, related_name="listingWatchlist")
    last_bidder_name = models.CharField(max_length=50, blank=True, null=True, default=None)
    def __str__(self):
        return self.name

class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True)
    bid_price = models.IntegerField(default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")
    bid_time = models.DateField() 

    def __str__(self):
        return f"{self.bidder} bid {self.bid_price} $ on {self.auction}"


class Comment(models.Model):
    content = models.CharField(max_length=160) 
    by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    on = models.DateField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")

    def __str__(self):
        return f"{self.by} made a comment at {self.on} to {self.listing}"

