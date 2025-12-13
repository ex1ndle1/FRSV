from django.db import models

# Create your models here.


class People(models.Model):
    
     image = models.ImageField(blank=True, null=False)
     name = models.CharField(max_length=250)
     last_name = models.CharField(max_length=25)
     role = models.CharField(default='student')

     




class PeopleEmb(models.Model):
     image = models.ImageField(upload_to='images/', blank=True, null = True, unique=True)
     name = models.CharField(max_length=240)
     vector = models.BinaryField(default=0)
 
