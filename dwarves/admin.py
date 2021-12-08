from django.contrib import admin
from .models import User, Mineral, Mine, Dwarf, Upgrade, Upgrade_owned, Job

# Register your models here.
admin.site.register(User)
admin.site.register(Mineral)
admin.site.register(Mine)
admin.site.register(Dwarf)
admin.site.register(Upgrade)
admin.site.register(Upgrade_owned)
admin.site.register(Job)



