from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


def set_default_datetime(days=30):
    return datetime.now(timezone.utc) + timedelta(days=days)


class Listing(models.Model):
    CATEGORY_CHOICES = [
        (0, ""),
        (1, "Fashion"),
        (2, "Toys"),
        (3, "Electronics"),
        (4, "Home")
    ]
    STATUS_CHOICES = [
        (0, "Open"),
        (1, "Closed"),
        (2, "Expired"),
        (3, "Sold")
    ]
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="listings")
    title = models.fields.CharField(max_length=128)
    description = models.fields.TextField(blank=True)
    image_url = models.fields.URLField(blank=True)
    # change choices to a model and use foreign key?
    category = models.fields.IntegerField(choices=CATEGORY_CHOICES, default=0)
    post_time = models.fields.DateTimeField(auto_now_add=True)
    # need override save method
    expire_time = models.fields.DateTimeField(default=set_default_datetime, editable=False)
    starting_bid = models.fields.DecimalField(max_digits=8, decimal_places=2)
    status = models.fields.IntegerField(choices=STATUS_CHOICES, default=0)


class Bid(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey("Listing", on_delete=models.SET_NULL, null=True, related_name="bids")
    post_time = models.fields.DateTimeField(auto_now_add=True)
    value = models.fields.DecimalField(max_digits=9, decimal_places=2)
    success = models.fields.BooleanField(default=False)


class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey("Listing", on_delete=models.SET_NULL, null=True, related_name="comments")
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="comments")
    post_time = models.fields.DateTimeField(auto_now_add=True)
    comment = models.fields.TextField()
    deleted = models.fields.BooleanField(default=False)
