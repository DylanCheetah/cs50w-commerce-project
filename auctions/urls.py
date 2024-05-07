from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create-listing"),
    path("view-listing/<int:id>", views.view_listing, name="view-listing"),
    path("watch/<int:id>", views.watch, name="watch"),
    path("unwatch/<int:id>", views.unwatch, name="unwatch"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close-bidding/<int:id>", views.close_bidding, name="close-bidding"),
    path("add-comment/<int:id>", views.add_comment, name="add-comment"),
    path("view-watchlist", views.view_watchlist, name="view-watchlist"),
    path("view-categories", views.view_categories, name="view-categories"),
    path("view-category/<int:id>", views.view_category, name="view-category")
]
