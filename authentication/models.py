from django.db import models

# Create your models here.
genre_choices = (
    ("Pop", "Pop"),
    ("Acoustic","Acoustic"),
    ("Ambient","Ambient"),
    ("Classical","Classical"),
    ("Instrumental","Instrumental"),
    ("Jazz","Jazz")
)

class Restaurant(models.Model):
    rest_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=genre_choices)
    performer = models.CharField(max_length=100, default="")
    ratings = models.CharField(max_length=100, default="")
    day = models.CharField(max_length=100, default="")
    time = models.CharField(max_length=100, default="")
    rest_image = models.ImageField(upload_to='restaurant', default="")

    
    # start_time = models.TimeField(null=True,blank=True)
    # end_time = models.TimeField(null=True,blank=True)

    def __str__(self):
        return self.rest_name