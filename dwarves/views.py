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
from django.core.exceptions import ObjectDoesNotExist

from random import random
from random import randint

from .models import User, Mineral, Mine, Dwarf, Upgrade, Upgrade_owned, Job, possible_minerals

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
    active_jobs = Job.objects.filter(dwarf__in=request.user.user_dwarfs.all())
    active_mines = []
    active_dwarves = []
    for job in active_jobs:
        active_dwarves.append(job.dwarf.name)
        active_mines.append(job.mine)
    inactive_dwarves = request.user.user_dwarfs.exclude(name__in=active_dwarves)
    return render(request, "dwarves/mining.html",{
        "mines" : mines,
        "active_mines" : active_mines,
        "active_jobs" : active_jobs,
        "inactive_dwarves" : inactive_dwarves,
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

def stop_mining(request, name):
    if request.method == "POST":
        active_jobs = Job.objects.filter(dwarf__in=request.user.user_dwarfs.all())
        current_job = active_jobs.get(mine=Mine.objects.get(name=name))
        drops = get_drops(current_job)
        current_job.delete()

        for drop in drops:
            try:
                mineral = request.user.inventory.get(name=drop[0])
            except ObjectDoesNotExist:
                mineral = Mineral(name=drop[0], user=request.user)
            mineral.value += drop[1]
            mineral.save()
            if drop[0] == "gold":
                request.user.gold_obtained += drop[1]
                request.user.save()
            if drop[1] != 0:
                messages.info(request, f"You have mined {drop[1]} {drop[0]}!")

    return redirect("mining")

# the algorithm to calculate the drops
def get_drops(job):
    time = (timezone.now() - job.start_time).seconds / 60
    drop_rate = job.mine.rate / 60
    minerals = job.mine.minerals.all()
    drops = []
    chances = calculate_chance(minerals, job.dwarf.discovery)
    total_value = 0
    for mineral in minerals:
        value = round((drop_rate * time * job.dwarf.speed) * chances[mineral.name])
        drops.append([mineral.name, value])
        total_value += value
    # shrink down drops if outside of capacity
    if job.dwarf.capacity < total_value:
        factor = job.dwarf.capacity/total_value
        drops = [[drop[0], round(drop[1]*factor)] for drop in drops]
    return drops

def calculate_chance(minerals, discovery):
    drop_table = {"common" : 0.68, "uncommon" : 0.25 * ((discovery - 1) * 0.5 + discovery),
                    "rare" : 0.06 * discovery, "very_rare" : 0.01 * discovery}
    chances = {}
    total_chance = 0
    for mineral in minerals:
        chance = drop_table[mineral.rarity] * random()
        chances[mineral.name] = chance
        total_chance += chance
    # standardize the chances to sum to 1
    for name in chances:
        chances[name] = chances[name] / total_chance
    return chances

class SelectionForm(forms.Form):
    dwarf = forms.CharField() 


def upgrading(request, name):
    try:
        dwarf = request.user.user_dwarfs.get(name = name)
    except ObjectDoesNotExist:
        return redirect("select")
    
    upgrades = Upgrade.objects.all()
    return render(request, "dwarves/upgrading.html",{
        "page_title" : f"Upgrading {name}",
        "dwarf" : dwarf,
        "upgrades" : upgrades,
    })



def select(request):
    dwarves_list = request.user.user_dwarfs.all()
    return render(request, "dwarves/select.html",{
        "page_title" : "Select a Dwarf for Upgrading",
        "dwarves" : dwarves_list
    })

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

        # create a users first dwarf
        dwarf = Dwarf(name=user.username, user=user, portrait = "portrait" + str(randint(1,amount_portraits)) + ".png")
        dwarf.save()
        mineral = Mineral(user=user, name="Gold", value=0)
        mineral.save()

        return HttpResponseRedirect(reverse("all_dwarves"))
    else:
        return render(request, "dwarves/register.html")
