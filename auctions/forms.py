from django import forms
from . import models


class ListingForm(forms.ModelForm):
    def validate_and_save(self, user):
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
    class Meta:
        model = models.Bid
        fields = ["value"]
        widgets = {
            "value": forms.NumberInput(attrs={"class": "form-control"})
        }
