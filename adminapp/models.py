from django.db import models



# Create your models here.

class Restaurant(models.Model):
    Restaurant_name=models.CharField(max_length=255)
    Image=models.ImageField(default='NULL')
    Description=models.CharField(max_length=255, default='NULL')
    Location=models.CharField(max_length=255)
    Rating=models.IntegerField()
    Time=models.IntegerField()
    Contact=models.IntegerField()
    Email=models.EmailField()


class Product(models.Model):
    # Image = models.ImageField()
    Name = models.CharField(max_length=255) 
    Description = models.TextField(max_length=255, default='NULL') 
    price = models.DecimalField(decimal_places=2,max_digits=7)   #2 digits after decimal,total no.including decimal
    Restaurant = models.ForeignKey('Restaurant',on_delete=models.CASCADE) #CASCADE::delete all products of that restaurant automatically:::'Restaurant', on_delete=models.CASCADE:::.Defines what happens if the linked restaurant is deleted.


class Coupon(models.Model):
    Coupon_name=models.CharField(max_length=255)
    Description=models.CharField(max_length=255)
    Discount=models.IntegerField()



    


    