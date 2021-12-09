from django.contrib import admin
from .models import User, Mineral, Mine, Dwarf, Upgrade, Upgrade_owned, Job

class MineralInline(admin.TabularInline):
    model = Mineral

class UpgradeAdmin(admin.ModelAdmin):
    inlines = [
        MineralInline,
    ]

class MineAdmin(admin.ModelAdmin):
    inlines = [
        MineralInline,
    ]

class UserAdmin(admin.ModelAdmin):
    inlines = [
        MineralInline,
    ]


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Mineral)
admin.site.register(Mine, MineAdmin)
admin.site.register(Dwarf)
admin.site.register(Upgrade, UpgradeAdmin)
admin.site.register(Upgrade_owned)
admin.site.register(Job)





