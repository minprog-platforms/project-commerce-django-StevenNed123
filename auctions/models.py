from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import FloatField, TextField
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass

class Listing(models.Model):
    user_id = ForeignKey(User,on_delete=CASCADE, related_name='user_listings')
    title = models.CharField(max_length=64)
    price = models.FloatField()
    description = models.CharField(max_length=200)
    date = models.DateField()
    image = models.URLField(max_length=200, default='', blank=True)
    closed = models.BooleanField(default=False)
    highest_bidder = ForeignKey(User, on_delete=CASCADE, related_name="winning_auctions", blank=True, null=True, default='')
    category = models.CharField(max_length=64, default='all purpose')

class Bid(models.Model):
    value = models.FloatField()
    listing_id = ForeignKey(Listing, related_name='listing_bids', on_delete=CASCADE)
    user_id = ForeignKey(User, related_name='user_bids',on_delete=CASCADE)
    date = models.DateField()

class Comment(models.Model):
    contents = models.TextField()
    listing_id = ForeignKey(Listing, related_name='listing_comments', on_delete=CASCADE)
    commenter = ForeignKey(User,on_delete=CASCADE, related_name='user_comments')
    date = models.DateField()

class Watchlist(models.Model):
    item = ForeignKey(Listing, related_name="watchlist_items", on_delete=CASCADE)
    person = ForeignKey(User, related_name="watchlist_users", on_delete=CASCADE)



