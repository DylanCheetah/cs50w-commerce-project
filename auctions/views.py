from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import AuctionCategory, AuctionListing, Bid, Comment, User


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.filter(is_active=True)
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
    

@login_required(login_url="/login")
def create_listing(request):
    # Handle submitted form data
    if request.method == "POST":
        # Fetch fields
        title = request.POST["title"]
        category = AuctionCategory.objects.get(pk=request.POST["category"])

        try:
            price = float(request.POST["price"])

        except ValueError:
            return render(request, "auctions/create-listing.html", {
                "categories": AuctionCategory.objects.all(),
                "message": "Price must be a number.",
                "data": request.POST
            })

        photo = request.POST["photo"]
        description = request.POST["description"]

        # Validate fields
        if len(title) == 0:
            return render(request, "auctions/create-listing.html", {
                "categories": AuctionCategory.objects.all(),
                "message": "Title must not be blank.",
                "data": request.POST
            })
        
        if category == "":
            return render(request, "auctions/create-listing.html", {
                "categories": AuctionCategory.objects.all(),
                "message": "You must choose a category.",
                "data": request.POST
            })
        
        if price < .01:
            return render(request, "auctions/create-listing.html", {
                "categories": AuctionCategory.objects.all(),
                "message": "Price must not be less than $0.01.",
                "data": request.POST
            })
        
        if len(description) == 0:
            return render(request, "auctions/create-listing.html", {
                "categories": AuctionCategory.objects.all(),
                "message": "Description must not be blank.",
                "data": request.POST
            })
        
        # Save auction listing
        listing = AuctionListing(
            title=title,
            category=category,
            seller=request.user,
            price=price,
            photo=photo,
            description=description
        )
        listing.save()

        # Redirect to homepage
        return HttpResponseRedirect(reverse("index"))

    # Display the auction listing form
    return render(request, "auctions/create-listing.html", {
        "categories": AuctionCategory.objects.all()
    })


def view_listing(request, id):
    listing = AuctionListing.objects.get(pk=id)
    return render(request, "auctions/view-listing.html", {
        "listing": listing,
        "is_watching": request.user.is_authenticated and request.user.is_watching(listing),
        "comments": listing.comments.all()
    })


@login_required(login_url="/login")
def watch(request, id):
    # Handle submitted form data
    if request.method == "POST":
        # Watch the listing with the given ID
        request.user.watchlist.add(AuctionListing.objects.get(pk=id))

    # Redirect to the watched view listing
    return HttpResponseRedirect(reverse("view-listing", args=[id]))


@login_required(login_url="/login")
def unwatch(request, id):
    # Handle submitted form data
    if request.method == "POST":
        # Unwatch the listing with the given ID
        request.user.watchlist.remove(AuctionListing.objects.get(pk=id))

    # Redirect to the unwatched view listing
    return HttpResponseRedirect(reverse("view-listing", args=[id]))


@login_required(login_url="/login")
def bid(request, id):
    # Handle submitted form data
    if request.method == "POST":
        # Fetch fields
        listing = AuctionListing.objects.get(pk=id)

        try:
            amount = float(request.POST["amount"])

        except ValueError:
            print("Bid amount must be a number.")
            return render(request, "auctions/view-listing.html", {
                "listing": listing,
                "is_watching": request.user.is_authenticated and request.user.is_watching(listing),
                "comments": listing.comments.all(),
                "bid_error": "Bid amount must be a number."
            })

        # Validate form data
        if amount <= listing.price:
            print("Bid amount must be greater than the current price of the item.")
            return render(request, "auctions/view-listing.html", {
                "listing": listing,
                "is_watching": request.user.is_authenticated and request.user.is_watching(listing),
                "comments": listing.comments.all(),
                "bid_error": "Bid amount must be greater than the current price of the item."
            })
        
        # Place the bid
        bid = Bid(user=request.user, auction_listing=listing, amount=amount)
        bid.save()

        # Update the listing price
        listing.price = amount
        listing.save()

    # Redirect to the view listing bidded upon
    return HttpResponseRedirect(reverse("view-listing", args=[id]))


@login_required(login_url="/login")
def close_bidding(request, id):
    # Handle submitted form data
    listing = AuctionListing.objects.get(pk=id)

    if request.method == "POST" and request.user == listing.seller:
        # Close the bidding
        listing.is_active = False
        listing.save()

    # Redirect to the closed listing
    return HttpResponseRedirect(reverse("view-listing", args=[id]))


@login_required(login_url="/login")
def add_comment(request, id):
    # Handle submitted form data
    if request.method == "POST":
        # Fetch fields
        text = request.POST["text"]

        # Add the new comment
        listing = AuctionListing.objects.get(pk=id)
        comment = Comment(user=request.user, auction_listing=listing, date=date.today(), text=text)
        comment.save()

    # Redirect to the listing page
    return HttpResponseRedirect(reverse("view-listing", args=[id]))


@login_required(login_url="/login")
def view_watchlist(request):
    return render(request, "auctions/view-watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })


def view_categories(request):
    return render(request, "auctions/view-categories.html", {
        "categories": AuctionCategory.objects.all()
    })


def view_category(request, id):
    category = AuctionCategory.objects.get(pk=id)
    return render(request, "auctions/view-category.html", {
        "category_name": category.name,
        "listings": category.items.filter(is_active=True)
    })
