from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    categories=models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.categories}"

class Listing(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="listinguser")
    name=models.CharField(max_length=64)
    price=models.IntegerField()
    image=models.URLField(max_length=400, blank=True)
    description=models.CharField(max_length=500, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="listcategory")

    def __str__(self):
        return f"{self.name} listed by {self.user} priced at {self.price}"
    
class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentuser")
    listing=models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commentlisting")
    comment=models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user} commented on {self.listing.name}"
    
class Bid(models.Model):
    listing=models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidlisting")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="biduser")
    bid=models.IntegerField(blank = True,)
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} bid {self.bid} on {self.listing.name}"
    
class Active(models.Model):
    listing=models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="activatelisting")
    active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.listing.name} is {self.active}"
    
class Watchlist(models.Model):
    listing=models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlistListing")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="userwatchlist")
    watchlist=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} watchlisted {self.listing.name}"