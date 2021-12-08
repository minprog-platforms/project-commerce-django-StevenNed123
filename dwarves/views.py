from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.fields import CharField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ModelForm 
from django import forms
from django.utils import timezone
from django.contrib import messages
from django.db.models import Max
from django.contrib.auth.decorators import login_required

from .models import User, Mineral, Mine, Dwarf, Upgrade, Upgrade_owned, Job

amount_portraits = 20

def all_dwarves(request):
    dwarves_list = Dwarf.objects.all()
    return render(request, "dwarves/all_dwarves.html",{
        "page_title" : "All Dwarves",
        "dwarves" : dwarves_list,
    })

def my_dwarves(request):
    dwarves_list = request.user.user_dwarfs.all()
    return render(request, "dwarves/all_dwarves.html",{
        "page_title" : "My Dwarves",
        "dwarves" : dwarves_list
    })

def leaderboard(request):
    users = User.objects.all()
    return render(request, "dwarves/leaderboard.html",{
        "users" : users
    })

 
def mining(request):
    mines = Mine.objects.all()
    dwarves = request.user.user_dwarfs.all()
    active_jobs = Job.objects.filter(dwarf__in=request.user.user_dwarfs.all())
    active_mines = []
    for job in active_jobs:
        active_mines.append(job.mine)
    return render(request, "dwarves/mining.html",{
        "mines" : mines,
        "dwarves" : dwarves,
        "active_mines" : active_mines,
        "active_jobs" : active_jobs,
    })

def start_mining(request, name):
    if request.method == "POST":
        form = SelectionForm(request.POST)
        if form.is_valid():
            dwarf_name = form.cleaned_data["dwarf"]
            dwarf = request.user.user_dwarfs.get(name = dwarf_name)
            mine = Mine.objects.get(name=name)
            new_job = Job(start_time = timezone.now(), dwarf=dwarf, mine=mine)
            new_job.save()
    return redirect("mining")
            

class SelectionForm(forms.Form):
    dwarf = forms.CharField() 


def upgrading(request):
    return render(request, "dwarves/upgrading.html")

def inventory(request):
    user_inventory = request.user.inventory.all()
    return render(request, "dwarves/inventory.html", {
        "inventory" : user_inventory,
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
            return HttpResponseRedirect(reverse("all_dwarves"))
        else:
            return render(request, "dwarves/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "dwarves/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("all_dwarves"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "dwarves/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "dwarves/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        return HttpResponseRedirect(reverse("all_dwarves"))
    else:
        return render(request, "dwarves/register.html")
