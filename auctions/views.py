from django.contrib.auth import authenticate, get_user, login, logout
from django.core.checks import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

def index(request):
    return render(request, "auctions/index.html",{
        'listings':Listing.objects.all(),
        'categories': Categories.objects.all()
    })

#def login_required(f):
 #   def wrapper(request):
  #      user = request.user
   #     if user is not None:
    #        return f(request)
     #   else:
      #      return render(request, "auctions/login.html")
    #return wrapper


def categories(request, cat_id):
    if cat_id == 'all':
        cat = Categories.objects.all()
        listing_list  =[Listing.objects.filter(category= _) for _ in cat]
        print( len(listing_list))
        
    else:
        cat = Categories.objects.filter(id=cat_id)
        listing_list = [Listing.objects.filter(category= _) for _ in cat_id]
        print(listing_list, len(listing_list))
    return render(request, "auctions/categories.html",{
            'categories': Categories.objects.all(),
            'category':cat,
            'listings':listing_list
        })    

@login_required(login_url='login')
def watchlist(request):
    user = User.objects.get(username= request.user)
    watchlist = user.watcher.all()
    
    return render(request, "auctions/watchlist.html",{
        'items': watchlist,
        'categories': Categories.objects.all()
    })

@login_required(login_url='login')
def add_to_watchlist(request, l_id):
    listing = Listing.objects.get(id=l_id)
    #create user istance
    user = User.objects.get(username=request.user)
    bids = listing.item.all()
    is_watched = user.watcher.filter(item=listing)
    if len(bids) > 0:
        top_bid = bids[len(bids)-1]

    if listing.status:
        message = "the auction is already close!"
        return render(request, 'auctions/listing.html',{
            'listing' : listing,
            'categories': Categories.objects.all(),
            'comments': listing.comments.all(),
            'message':message
        })
    else:
        if is_watched:
            is_watched.delete()
            message = "the item has been removed from your watchlist!"
            return render(request, 'auctions/listing.html',{
                'listing' : listing,
                'categories': Categories.objects.all(),
                'comments': listing.comments.all(),
                'bids':BidForm(),
                'message':message,
                'top_bid': top_bid,
                'is_watched':False
            })
            print('ok')
        else:
            #create Watchlist istance
            watchlist = WatchList(user=user, item=listing)
            watchlist.save()
            message = "Item added to your watchlist!"
            return render(request, 'auctions/listing.html',{
                'listing' : listing,
                'categories': Categories.objects.all(),
                'comments': listing.comments.all(),
                'bids':BidForm(),
                'message':message,
                'top_bid': top_bid ,
                'is_watched':True
            })
    return HttpResponseRedirect(reverse('listing', args=(l_id)))

@login_required(login_url='login')
def new_listing(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.creator = user
            f.save()
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'auctions/new_listing.html',{
        'form':ListingForm(),
        'categories': Categories.objects.all(),
        'cat':CategoryForm()
    })
@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        cat = CategoryForm(request.POST)
        if cat.is_valid():
            cat.save()
        else:
            pass
        return HttpResponseRedirect(reverse('new_listing'))
    return HttpResponseRedirect(reverse('index'))

def listing(request, listing_id):

    listing = Listing.objects.get(id=listing_id)
    bid = BidForm()    
    bid.fields['price'].initial = listing.starting_bid
    comments = listing.comments.all()
    top_bid = listing.item.all()
    try:
        user = User.objects.get(username= request.user)
    
        is_watched = user.watcher.filter(item=listing)
        if is_watched:
            _= True
        else:
            _= False
    except:
        _ = False

    if len(top_bid) > 0:
        return render(request, 'auctions/listing.html',{
            'listing':listing,
            'categories': Categories.objects.all(),
            'bids':bid,
            'comments':comments,
            'top_bid':top_bid[len(top_bid)-1],
            'is_watched': _
        })
    return render(request, 'auctions/listing.html',{
            'listing':listing,
            'categories': Categories.objects.all(),
            'bids':bid,
            'comments':comments,
            'is_watched': _
        })

@login_required(login_url='login')
def close_auction(request, l_id):
    listing = Listing.objects.get(id= l_id)
    listing.status = True
    listing.save()
    return HttpResponseRedirect(reverse('listing',args=(l_id)))

@login_required(login_url='login')
def new_bid(request, l_id):
    listing = Listing.objects.get(id=l_id)
    bids = BidForm(request.POST)
    user = User.objects.get(username=request.user)
    
    if request.method == "POST":
        new_bid = float(request.POST['price'])
        current_price = listing.starting_bid
        if new_bid > current_price:
            bid = bids.save(commit=False)
            bid.user = user
            bid.save()
            listing.item.add(bid)
            listing.starting_bid = new_bid
            listing.save()
            return HttpResponseRedirect(reverse('listing',args=(),kwargs={'listing_id':l_id}))
        else:
             return render(request, 'auctions/listing.html',{
            'listing':listing,
            'categories': Categories.objects.all(),
            'bids':BidForm(),
            'comments':listing.comments.all(),
            'message': 'error! the bid is not valid! try again with a bigger bid than the actual price!'
        })
@login_required(login_url='login')
def comments(request, l_id):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        user = User.objects.get(username=request.user)
        listing = Listing.objects.get(id=l_id)
        if title and body:
            comment= Comment(title=title,comment=body)
            comment.user = user
            comment.save()
            listing.comments.add(comment)
            listing.save()
        return HttpResponseRedirect(reverse('listing',args=(),kwargs={'listing_id':l_id}))
    
    pass


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
                "message": "Invalid username and/or password.",
                'categories': Categories.objects.all(),                
            })
    else:
        return render(request, "auctions/login.html",{
            'categories': Categories.objects.all(),
        })


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
                "message": "Passwords must match.",
                'categories': Categories.objects.all(),
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                'categories': Categories.objects.all(),
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html",{
            'categories': Categories.objects.all(),
        })
