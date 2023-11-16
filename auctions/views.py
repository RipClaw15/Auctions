from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from datetime import date

from .models import User, Listing, Bid, Comment 


def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
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

def create(request):
    if request.method == "POST":
        currentUser = request.user
        name = request.POST["name"]
        price = request.POST["price"]
        description = request.POST["description"]
        category = request.POST["category"]
        image_url = request.POST["image_url"]
        listed_on = date.today()
        created_by = request.POST["created_by"]
        is_active = True

        bid = Bid(bid_price=int(price), bidder = currentUser, bid_time = listed_on)
        bid.save()

        listing = Listing.objects.create(name=name, 
                                 price=price, 
                                 description=description, 
                                 category=category, 
                                 image_url=image_url, 
                                 listed_on=listed_on, 
                                 created_by=currentUser,
                                 is_active=is_active)
        listing.save()
        
    return render(request, "auctions/create.html")

def listed_item(request, id):
    item = get_object_or_404(Listing, pk=id)
    isListingInWatchlist = request.user in item.watchlist.all()
    allComments = Comment.objects.filter(listing=item)
    isOwner = request.user.username == item.created_by.username
    return render(request, 'auctions/item.html', {
        'item': item,
        'isListingInWatchlist': isListingInWatchlist,
        'allComments': allComments,
        'isOwner': isOwner
        })

def displayWatchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    
    return render(request, "auctions/watchlist.html",
                  {
                      "listings":listings
                  })

def addWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listed_item",args=(id, )))

def removeWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listed_item",args=(id, )))

def category(request):
    category_id = request.GET.get('category_id')
    currentUser = request.user
    listings = Listing.objects.filter(category=category_id,is_active=True)
    return render(request, "auctions/category.html",
                  {
                      "listings":listings,
                      "category":category_id
                  })

def my_listings(request):
    currentUser = request.user
    active_listings = Listing.objects.filter(created_by=currentUser, is_active=True)
    return render(request, "auctions/category.html",
                  {
                      "listings":active_listings,
                      "category":"My Listings"
                  })

def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']

    newComment = Comment(
        content = message,
        by = currentUser,
        on = date.today(),
        listing = listingData
    )

    newComment.save()

    return HttpResponseRedirect(reverse("listed_item",args=(id, )))

def addBid(request, id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    listing_instance = Listing.objects.get(name=listingData.name)
    isOwner = request.user.username == listingData.created_by
    if newBid:
        if listingData.created_by == request.user:
            return render(request, "auctions/item.html",{
                "item": listingData,
                "message": "You cannot make bids on your own auctions!",
                "update": 0,
                "isOwner": isOwner,
                "isListingInWatchlist":isListingInWatchlist,
                "allComments": allComments
            })

        if int(newBid) > listingData.price:
            
            updateBid = Bid(bidder=request.user, 
                            bid_price=int(newBid), 
                            bid_time= date.today(),
                            auction=listing_instance)
            
            updateBid.save()
            if not isListingInWatchlist:
                listingData.watchlist.add(request.user)
            listingData.price = updateBid.bid_price
            listingData.last_bidder_name = request.user.username
            listingData.save()
            return render(request, "auctions/item.html",{
                "item": listingData,
                "message": "You are winning this bid",
                "update": 1,
                "isOwner": isOwner,
                "isListingInWatchlist":isListingInWatchlist,
                "allComments": allComments
            })
        else:
            return render(request, "auctions/item.html",{
                "item": listingData,
                "message": "Your bid is not bigger then the current price",
                "update": 0,
                "isOwner": isOwner,
                "isListingInWatchlist":isListingInWatchlist,
                "allComments": allComments
            })
    else: 
            return render(request, "auctions/item.html",{
                "item": listingData,
                "message": "Enter a valid bid",
                "update": False
            })
    
def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.is_active = False
    listingData.save()
    isListingInWatchlist = request.user in listingData.watchlist.all()        
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = listingData.created_by == request.user
    return render(request, "auctions/item.html",{
        "item": listingData,
        "message": "Your auction was closed",
        "update": 1,
        "isOwner": isOwner,
        "isListingInWatchlist":isListingInWatchlist,
        "allComments": allComments
    }) 