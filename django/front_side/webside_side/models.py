from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import random, os


def photo_path(instance, filename):
    file_extension= os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10)).upper()
    res = 'images/{name}_{date}/{name}_{randomstring}{ext}'.format(name=instance.title.replace(' ','_'), date=instance.date, userid= instance.author.id, randomstring=randomstr, ext=file_extension)
    print(randomstr.upper())
    return res

#random function
location = "New York, NY, United States"

body_types = [
    ('Sedan','Sedan'),
    ('Classic','Classic'),
    ('Sport','Sport'),
    ('Coupe','Coupe'),
    ('Wagon','Wagon'),
    ('Hatchback','Hatchback'),
    ('Convertible','Convertible'),
    ('SUV','SUV'),
    ('Mini Van','Mini Van'),
    ('Pickup Truck','Pickup Truck'),
]

transmission_type = [
    ('Automatic','Automatic'),
    ('Manual','Manual'),
]

seller_type = [
    ('Dealer','Dealer'),
    ('Seller','Seller'),
]

fuel_type = [
    ('Gasoline','Gasoline'),
    ('Petrol','Petrol'),
]

status_type = [
    ('Active','Active'),
    ('Inactive','Inactive'),
    ('Sold','Sold'),
]

featured_type = [
    ('Yes', 'Yes'),
    ('No','No')
]


class WebSiteName(models.Model):
    website =  models.CharField(max_length=255,default='CARRRRRR')

    def __str__(self) -> str:
        return f'{self.website}'
    
    #def get_absolute_url(self):
        #return reverse('item_detail', args=(str(self.id)) ) 
     #   return reverse('home') 

class Category(models.Model):
    name =  models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.name}'
    
    def get_absolute_url(self):
        #return reverse('item_detail', args=(str(self.id)) ) 
        return reverse('home') 

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.CharField(max_length=10, default='Seller',  choices=seller_type)

    def __str__(self) -> str:
        return f'{self.user}'  

    def get_absolute_url(self):
        return reverse('home', args=[str(self.id)]) 


class Post(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=255, default=location)
    make = models.CharField(max_length=33)
    year = models.IntegerField()
    bodytype = models.CharField(max_length=15, choices=body_types)
    transmission = models.CharField(max_length=10, choices=transmission_type)
    itemStatus = models.CharField(max_length=8, choices=status_type)
    fuelType = models.CharField(max_length=10, choices=fuel_type)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    miles = models.DecimalField(max_digits=10, decimal_places=0)
    color = models.CharField(max_length=15, default="Blue")
    engine = models.IntegerField()
    description = models.TextField()
    alloyWheels = models.BooleanField(default=True)
    air = models.BooleanField(default=False)
    radio = models.BooleanField(default=False)
    abs = models.BooleanField(default=False)
    featured = models.CharField(max_length=3,choices=featured_type)
    powerLocks = models.BooleanField(default=False)
    powerWindows = models.BooleanField(default=False)
    cd = models.BooleanField(default=False)
    bonnet = models.BooleanField(default=False)
    airBags = models.BooleanField(default=False)
    coolBox = models.BooleanField(default=False)
    powerSteering = models.BooleanField(default=False)
    category  = models.CharField(max_length=15)
    image1 = models.ImageField(null=True, blank=True, upload_to=photo_path, default="default.jpg")
    image2 = models.ImageField(null=True, blank=True, upload_to=photo_path, default="default.jpg")
    image3 = models.ImageField(null=True, blank=True, upload_to=photo_path, default="default.jpg")
    image4 = models.ImageField(null=True, blank=True, upload_to=photo_path, default="default.jpg")
    image5 = models.ImageField(null=True, blank=True, upload_to=photo_path, default="default.jpg")
    bio = models.CharField(max_length=10, default='Dealer',  choices=seller_type)
    
    def __str__(self) :
        return f'{self.title} | {self.author}'
    
    def get_absolute_url(self):
          #id = str(self.id)
        return reverse('item_detail', args=[str(self.id)]) 
        #return reverse('home') 
    
