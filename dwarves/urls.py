from django.urls import path

from . import views

urlpatterns = [
    path("", views.all_dwarves, name="all_dwarves"),
    path("my_dwarves", views.my_dwarves, name="my_dwarves"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("mining", views.mining, name="mining"),
    path("upgrading/<str:name>", views.upgrading, name="upgrading"),
    path("inventory", views.inventory, name="inventory"),
    path("start_mining/<str:name>", views.start_mining, name="start_mining"),
    path("stop_mining/<str:name>", views.stop_mining, name="stop_mining"),
    path("select", views.select, name="select"),
]
