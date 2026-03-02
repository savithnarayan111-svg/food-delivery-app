from django.db import models
from django.contrib.auth.models import User
from adminapp.models import Product,Restaurant

# Create your models here.
# class SignUp(models.Model):
#     Name=models.CharField(max_length=250)
#     Email=models.EmailField()
#     Age = models.IntegerField()
#     Phone=models.IntegerField()
#     Password=models.CharField(max_length=1000)
class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


#ADD_ON CLASS
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Address=models.CharField(max_length=255)
    Zipcode=models.IntegerField()
    Phone=models.IntegerField()

class Wishlist(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Rating=models.PositiveIntegerField()
    Review=models.CharField(max_length=255)


class RestaurantReview(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    Rating=models.PositiveIntegerField()
    Review=models.CharField(max_length=255)
    
#