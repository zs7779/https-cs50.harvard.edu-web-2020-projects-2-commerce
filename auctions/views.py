from datetime import datetime, timezone
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage

from . import models, forms


@login_required
def index(request):
    return render(request, "auctions/index.html", {
        "listings": models.Listing.objects.all()
    })


@login_required
def listing(request, listing_id):
    if request.method == "GET":
        item = models.Listing.objects.get(id=listing_id)
        return render(request, "auctions/listing.html", {
            "listing": {
                "user": item.user,
                "title": item.title,
                "description": item.description,
                "image_url": item.image_url,
                "category": item.get_category_display(),
                "post_time": item.post_time,
                "expire_time": item.expire_time,
                "starting_bid": item.starting_bid,
                "status": item.get_status_display()
            },
            "is_owner": request.user.id == item.user.id,
            "form": forms.BiddingForm(),
            "image_placeholder_url": staticfiles_storage.url('auctions/image-placeholder.jpg')
        })
    elif request.method == "POST":
        pass


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
            form = form.validate_and_save(request.user)
            return redirect("listing", id=form.id)
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
