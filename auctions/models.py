from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField


class User(AbstractUser):
    pass

class Categories(models.Model):
    categories = models.CharField(max_length=50, null=True,unique=True)
   
    def __str__(self):
        return f'{self.categories}'


class Comment(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=50)
    comment = models.TextField(max_length=500)
    time =models.DateTimeField(auto_now_add=True, blank=True)
    

    def __str__(self):
        return self.title

class Listing(models.Model):
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    starting_bid = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(blank=True,null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE,blank=True, null=True, related_name='categ')
    comments = models.ManyToManyField(Comment, blank=True, related_name='comments')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Bid(models.Model):

    time = models.DateTimeField(auto_now=True )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bider')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bid = models.ManyToManyField(Listing, blank=True, related_name='item'  )

    def __str__(self):
        return f"user {self.user} bid: {self.price} at {self.time}"

class WatchList(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watcher')
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watch')