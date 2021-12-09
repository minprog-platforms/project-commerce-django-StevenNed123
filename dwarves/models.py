from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT
from django.db.models.expressions import F
from django.db.models.fields import CharField, FloatField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.utils import timezone


possible_minerals = [('Gold', 'gold'), ('Iron', 'iron') ,('Marble', 'marble'), ('Quartz', 'quartz')]

class User(AbstractUser):
    gold_obtained = models.IntegerField(default=0)

class Mine(models.Model):
    name = models.CharField(max_length=64)
    rate = models.IntegerField(default=0)
    requirement = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.name}"

class Dwarf(models.Model):
    name = models.CharField(max_length=64)
    user = ForeignKey(User, related_name="user_dwarfs", on_delete=CASCADE)
    portrait = models.CharField(max_length=64,default="portrait1.png")
    speed = FloatField(default=1)
    capacity = models.IntegerField(default=100)
    discovery = FloatField(default=1)
    def __str__(self):
        return f"{self.user}, {self.name}"

class Job(models.Model):
    mine = ForeignKey(Mine, on_delete=CASCADE, related_name="mine_jobs")
    dwarf = ForeignKey(Dwarf, on_delete=CASCADE, related_name="dwarf_jobs")
    start_time = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return f"{self.dwarf} in {self.mine}"


class Upgrade(models.Model):
    name = CharField(max_length=64)
    speed = FloatField(default=0)
    capacity = IntegerField(default=0)
    discovery = FloatField(default=0)
    requirement = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.name}"

class Upgrade_owned(models.Model):
    dwarf = ForeignKey(Dwarf, related_name="dwarf_upgrades", on_delete=CASCADE)
    upgrade = ForeignKey(Upgrade, related_name="upgrade_dwarfs", on_delete=CASCADE)
    amount_owned = IntegerField(default=0)
    def __str__(self):
        return f"{self.upgrade}, {self.dwarf}"

class Mineral(models.Model):
    user = ForeignKey(User,blank=True, null=True, default="", on_delete=CASCADE, related_name="inventory")
    upgrade = ForeignKey(Upgrade,blank=True, null=True, default="", on_delete=CASCADE, related_name="cost")
    mine = ForeignKey(Mine,blank=True, null=True, default="", on_delete=CASCADE, related_name="minerals")
    name = models.CharField(max_length=64, choices=possible_minerals)
    value = models.IntegerField(blank=True, null=True, default=0)
    rarity = models.CharField(max_length=64, blank=True, null=True, default='', choices=[
        ('', ''), ('common', 'Common') ,('uncommon', 'Uncommon'), ('rare', 'Rare'), ('very_rare', 'Very Rare')])
    def __str__(self):
        if self.user != None:
            return f"{self.user}, {self.name}, {self.value},"
        elif self.upgrade != None:
            return f"{self.upgrade}, {self.name}, {self.value}"
        else:
            return f"{self.mine}, {self.name}, {self.rarity}"




