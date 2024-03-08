from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
genre_choices = (
    ("Pop", "Pop"),
    ("Acoustic","Acoustic"),
    ("Ambient","Ambient"),
    ("Classical","Classical"),
    ("Instrumental","Instrumental"),
    ("Jazz","Jazz")
)

day_choices = (
    ("Sunday", "Sunday"),
    ("Monday","Monday"),
    ("Tuesday","Tuesday"),
    ("Wednesday","Wednesday"),
    ("Thursday","Thursday"),
    ("Friday","Friday"),
    ("Saturday","Saturday")
)


class Restaurant(models.Model):
    rest_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=genre_choices)
    performer = models.CharField(max_length=100, default="")
    ratings = models.CharField(max_length=100, default="")
    # day = models.CharField(max_length=100, default="")
    # time = models.CharField(max_length=100, default="")

    day = models.CharField(max_length=100, choices=day_choices)
    
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)

    rest_image = models.ImageField(upload_to='restaurant', default="")
    def __str__(self):
        return self.rest_name
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant') 
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    rated_date=models.DateTimeField(default=datetime.now)
    def __str__(self):
        return str(self.pk)