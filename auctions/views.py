from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import User, Listing, Comment, Category, Bid, Active, Watchlist


def index(request):
    active_listings = Listing.objects.filter(activatelisting__active=True)
    for list in active_listings:
        bid=Bid.objects.filter(listing=list)
        highest_bid = bid.order_by('-bid').first()
        list.current_price = highest_bid.bid if highest_bid else list.price
    return render(request, "auctions/index.html", {
        "listing": active_listings,
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


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing=listing)
    bid = Bid.objects.filter(listing=listing).order_by('-bid')
    active = Active.objects.get(listing=listing)
    user=request.user
    try:
        watchlist = Watchlist.objects.get(user=request.user, listing=listing)
    except Watchlist.DoesNotExist:
        watchlist = None
    if bid.exists():
        bidder = bid.first().user
        return render(request, "auctions/listing.html", {
            "listing":listing,
            "comments":comments,
            "user":user,
            "bidder":bidder,
            "check":True,
            "active":active.active,
            "watchlist":watchlist.watchlist if watchlist else False
        })
    else :
        price=listing.price
        return render(request, "auctions/listing.html", {
            "listing":listing,
            "comments":comments,
            "user":user,
            "check":False,
            "active":active.active,
            "watchlist":watchlist.watchlist if watchlist else False
        })


def place_bid(request, listing_id):
    listing=Listing.objects.get(pk=listing_id)
    bid=Bid.objects.filter(listing=listing).order_by('-bid')
    if request.method == 'POST':
        bid_amount = int(request.POST.get('bid_amount'))
        if bid.exists():
            highest_bid = bid.first()
            if bid_amount <= listing.price:
                messages.error(request, "Your bid must be higher than the starting price.")
            elif bid_amount <= highest_bid.bid:
                messages.error(request, "Your bid must be higher than the current highest bid.")
            else:
                new_bid = Bid(listing=listing, user=request.user, bid=bid_amount)
                new_bid.save()

                listing.price = bid_amount
                listing.save()

                messages.success(request, "Your bid was placed successfully!")
        else:
            if bid_amount <= listing.price:
                messages.error(request, "Your bid must be higher than the starting price.")
            else:
                new_bid = Bid(listing=listing, user=request.user, bid=bid_amount)
                new_bid.save()

                listing.price = bid_amount
                listing.save()

                messages.success(request, "Your bid was placed successfully!")

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def add_comment(request, listing_id):
    listing=Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        new_comment= Comment(listing=listing, user=request.user, comment=request.POST['new_comment'])
        new_comment.save()

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
def close_bid(request, listing_id):
    listing=Listing.objects.get(pk=listing_id)
    active=Active.objects.get(listing=listing)
    if request.method == "POST":
        active.active=False
        active.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def watchlist(request):
    watchlist_listings = Watchlist.objects.filter(user=request.user, watchlist=True)

    listings = [watchlist_item.listing for watchlist_item in watchlist_listings]

    for list in listings:
        bid=Bid.objects.filter(listing=list)
        highest_bid = bid.order_by('-bid').first()
        list.current_price = highest_bid.bid if highest_bid else list.price
    return render(request, "auctions/watchlist.html", {
        "listing": listings,
    })

def add_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watchlist=Watchlist.objects.filter(listing=listing)
    if request.method == "POST":
        if watchlist:
            watchlist[0].watchlist=True
            watchlist[0].save()
        else:
            new_watchlist = Watchlist(listing=listing, user=request.user, watchlist=True)
            new_watchlist.save()

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watchlist=Watchlist.objects.get(listing=listing)
    if request.method == "POST":
        watchlist.watchlist=False
        watchlist.save()

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
 
def make_listing(request):
    categories=Category.objects.all()
    if request.method=="POST":
        name=request.POST['name']
        price=request.POST['price']
        image=request.POST['image']
        description=request.POST['description']
        category_id=request.POST['category']
        
        category = Category.objects.get(id=category_id) if category_id else None

        listing=Listing(user = request.user, name=name, price=price, image=image, description=description, category=category)
        listing.save()

        new_active=Active(listing=listing, active=True)
        new_active.save()

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    
    return render(request, "auctions/makelisting.html",{
        "categories":categories
    })


# def categories(request):
#     categories=Category.objects.all()
#     return render(request, "auctions/categories.html", {
#         "categories":categories
#     })

# def category(request, category_id):
#     listing=Listing.listcategory.filter(categories=Category.objects.get(pk=category_id))
#     active_listings = listing.objects.filter(activatelisting__active=True)
#     for list in active_listings:
#         bid=Bid.objects.filter(listing=list)
#         highest_bid = bid.order_by('-bid').first()
#         list.current_price = highest_bid.bid if highest_bid else list.price
#     return render(request, "auctions/index.html", {
#         "listing": active_listings,
#     })
