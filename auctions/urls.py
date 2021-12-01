from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:name>", views.listing, name="listing"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:name>", views.categories_index, name="categories_index")
]
