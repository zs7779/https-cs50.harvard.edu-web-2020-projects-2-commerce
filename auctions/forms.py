from django import forms
from . import models


class ListingForm(forms.ModelForm):
    def save_user(self, user):
        listing = self.save(commit=False)
        listing.user = user
        listing.save()
        return listing

    class Meta:
        model = models.Listing
        exclude = ["user", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "image_url": forms.URLInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "starting_bid": forms.NumberInput(attrs={"class": "form-control"})
        }


class BiddingForm(forms.ModelForm):
    def save_user_listing(self, user, listing):
        bid = self.save(commit=False)
        bid.user = user
        bid.listing = listing
        bid.save()
        return bid

    class Meta:
        model = models.Bid
        fields = ["value"]
        widgets = {
            "value": forms.NumberInput(attrs={"class": "form-control", "step": 1.00, "width": "10px"})
        }
