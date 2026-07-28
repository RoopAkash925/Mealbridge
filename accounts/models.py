from django.db import models
from django.contrib.auth.models import User



class Home(models.Model):

    HOME_TYPES = [
        ('Old Age Home', 'Old Age Home'),
        ('Orphanage', 'Orphanage'),
        ('Shelter', 'Shelter'),
        ('NGO', 'NGO'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    organization_name = models.CharField(max_length=200)
    home_type = models.CharField(max_length=50, choices=HOME_TYPES)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    residents = models.IntegerField()
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.organization_name
    




class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Donation(models.Model):

    donor = models.ForeignKey(User, on_delete=models.CASCADE)

    event_name = models.CharField(max_length=200)
    food_type = models.CharField(max_length=50)
    quantity = models.IntegerField()
    cooked_time = models.TimeField(null=True, blank=True)
    pickup_deadline = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)
    packaging = models.CharField(max_length=100)
    image = models.ImageField(upload_to="donations/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name