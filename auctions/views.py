from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ModelForm 
from django import forms
from django.utils import timezone
from django.contrib import messages
from django.db.models import Max
from django.contrib.auth.decorators import login_required

from .models import Listing, User, Bid, Comment, Watchlist

possible_categories = [
            ('AP', 'All Purpose'),
            ('SP', 'Sport'),
            ('EL', 'Electronics'),
            ('FA', 'Fashion'),
            ('CO', 'Cooking'),]

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings" : listings,
        "title" : "Active Listings"
    })

@login_required(login_url='login')
def my_listings(request):
    listings = Listing.objects.filter(user_id=request.user)
    return render(request, "auctions/index.html", {
        "listings" : listings,
        "title" : "My Listings"
    })

@login_required(login_url='login')
def watchlist(request):

    items = request.user.watchlist_users.all()
    listings = []
    for listing in items:
        listings.append(listing.item)
        
    return render(request, "auctions/index.html", {
        "listings" : listings,
        "title" : "Watchlist"
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories" : [x[1] for x in possible_categories],
    })

def categories_index(request, name):
    listings = Listing.objects.filter(category=name)
    return render(request, "auctions/index.html",{
        "listings" : listings,
        "title" : "Category: " + name
    })


def listing(request, name):
    if request.method == "POST":

        if 'bid' in request.POST:
            form = BidForm(request.POST)
            if form.is_valid():
                listing = Listing.objects.get(title=name)
                value = form.cleaned_data["value"]
                if value > listing.price:
                    listing.price = value
                    listing.highest_bidder = request.user
                    listing.save()
                    new = Bid(value=value, listing_id=listing,
                                user_id=request.user, date=timezone.now())
                    new.save()
                    return redirect("listing", name=listing.title)
                else:
                    messages.error(request, f"Bid of {value} is lower than the current price of {listing.price}")
                    return redirect("listing", name=listing.title)

        elif 'comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                listing = Listing.objects.get(title=name)
                contents = form.cleaned_data["contents"]
                new = Comment(listing_id=listing, contents=contents, commenter=request.user, date=timezone.now())
                new.save()
                return redirect("listing", name=listing.title)
        
        elif 'close' in request.POST:
            listing = Listing.objects.get(title=name)
            listing.closed = True
            listing.save()
            return redirect("listing", name=listing.title)
        
        elif 'add_watchlist' in request.POST:
            listing = Listing.objects.get(title=name)
            user = request.user
            new = Watchlist(item=listing, person=user)
            new.save()
            return redirect("listing", name=listing.title)

        elif 'remove_watchlist' in request.POST:
            listing = Listing.objects.get(title=name)
            user = request.user
            Watchlist.objects.filter(person=request.user, item=listing).delete()
            return redirect("listing", name=listing.title)

    listing = Listing.objects.get(title=name)
    comments = listing.listing_comments.all()
    watchlist = []
    if request.user.is_authenticated:
        items = request.user.watchlist_users.all()
        for item in items:
            watchlist.append(item.item)
    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "comments" : comments,
        "form" : BidForm(),
        "commentform" : CommentForm(),
        "watchlist" : watchlist
    })

@login_required(login_url='login')
def create_listing(request):    
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            category = form.cleaned_data["category"]
            new = Listing(title=title, price=form.cleaned_data["price"],
                        description = form.cleaned_data["description"], image = form.cleaned_data["image"],
                        date=timezone.now(), user_id=request.user, category=dict(form.fields['category'].choices)[category])
            new.save()
            return redirect("listing", name=title)

    return render(request, "auctions/create_listing.html", {
        "form" : ListingForm(),
    })

class ListingForm(forms.Form):
    title = forms.CharField()
    price = forms.FloatField()
    description = forms.CharField()
    image = forms.URLField(required=False)
    category = forms.ChoiceField(choices=possible_categories)

class BidForm(forms.Form):
    value = forms.FloatField()


class CommentForm(forms.Form):
    contents = forms.CharField(label="Comment on this listing:", widget=forms.Textarea(attrs={"placeholder":"comment goes here"}))
    

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
