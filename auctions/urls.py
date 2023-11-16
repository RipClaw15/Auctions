from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:id>/", views.listed_item, name="listed_item"),
    path("create", views.create, name="create"),
    path("watchlist", views.displayWatchlist, name="watchlist"),
    path("category", views.category, name="category"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist")
]
