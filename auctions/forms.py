from django import forms
from django.db.models import fields
from django.forms import ModelForm, widgets
from .models import *


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description', 'starting_bid','category', 'image']
class CategoryForm(ModelForm):
    class Meta:
        model = Categories
        fields = ['categories']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']

      