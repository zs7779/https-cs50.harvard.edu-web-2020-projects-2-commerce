from datetime import datetime, timezone
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage

from . import models, forms
from .listing_status import STATUS_COLORS


@login_required
def index(request, category=""):
    category_code = 0
    try:
        if category != "":
            category_code = models.Category.objects.get(category=category).id
    except models.Category.DoesNotExist:
        return redirect("index")

    items = models.Listing.objects.filter(status=0)
    if category_code != 0:
        items = items.filter(category=category_code)
    items = [{
        "id": item.id,
        "user": item.user,
        "title": item.title,
        "description": item.description,
        "image_url": item.image_url,
        "post_time": item.post_time,
        "status": item.get_status_display(),
        "status_color": STATUS_COLORS[item.status],
        "starting_bid": item.starting_bid,
        "bids": item.bids.order_by("-value")[:1]
    } for item in items]
    watches = models.Bid.objects.filter(value=None, user=request.user)
    return render(request, "auctions/index.html", {
        "category": category,
        "listings": items,
        "watches": watches,
        "image_placeholder_url": staticfiles_storage.url('auctions/image-placeholder.jpg'),
        "categories": models.Category.objects.all()
    })


@login_required
def listing(request, listing_id):
    try:
        item = models.Listing.objects.get(id=listing_id)
    except models.Listing.DoesNotExist:
        raise Http404("Listing does not exist")

    watches = models.Bid.objects.filter(listing=item)
    high_bid = watches.exclude(value=None).order_by("-value")[:1]
    my_bid = watches.exclude(value=None, user=request.user).order_by("-value")[:1]
    my_watch = watches.filter(value=None, user=request.user)[:1]
    if request.method == "GET":
        if len(my_bid) != 0:
            form = forms.BiddingForm(instance=my_bid[0])
        else:
            form = forms.BiddingForm()
        return render(request, "auctions/listing.html", {
            "listing": {
                "id": listing_id,
                "user": item.user,
                "title": item.title,
                "description": item.description,
                "image_url": item.image_url,
                "post_time": item.post_time,
                "expire_time": item.expire_time,
                "starting_bid": item.starting_bid,
                "high_bid": high_bid,
                "watch": my_watch,
                "status": item.get_status_display(),
                "status_color": STATUS_COLORS[item.status],
                "is_owner": request.user.id == item.user.id,
            },
            "category": item.get_category_display(),
            "form": form,
            "image_placeholder_url": staticfiles_storage.url('auctions/image-placeholder.jpg')
        })
    elif request.method == "POST":
        form = forms.BiddingForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["value"] is None:
                if item.status == 0 and request.user == item.user:
                    high_bid = watches.exclude(value=None).order_by("-value")[:1]
                    if len(high_bid) > 0:
                        item.status = 3
                    else:
                        item.status = 1
                    item.save()
                elif len(my_watch) != 0:
                    my_watch[0].delete()
                else:
                    form = form.save_user_listing(request.user, item)
            elif item.status == 0 and len(high_bid) == 0 or form.cleaned_data["value"] > high_bid[0].value:
                form = form.save_user_listing(request.user, item)
        return redirect("listing", listing_id=listing_id)


@login_required
def new_listing(request):
    if request.method == "GET":
        form = forms.ListingForm()
        return render(request, "auctions/new_listing.html", {
            "form": form
        })
    elif request.method == "POST":
        form = forms.ListingForm(request.POST)
        if form.is_valid():
            form = form.save_user(request.user)
            return redirect("listing", listing_id=form.id)
        else:
            return render(request, "auctions/new_listing.html", {
                "form": form
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
            user = models.User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
