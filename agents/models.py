from django.db import models

# Create your models here.

def upload_location(instance, filename):
	  return "%s/%s" %(instance, filename)


class Agent(models.Model):
    name = models.CharField(max_length=225)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=225, null=True, blank=True)
    address = models.CharField(max_length=225, null=True, blank=True)
    city = models.CharField(max_length=225, null=True, blank=True)
    country = models.CharField(max_length=225, null=True, blank=True)
    zip_code = models.CharField(max_length=225, null=True, blank=True)
    state = models.CharField(max_length=225, null=True, blank=True)
    image = models.ImageField(upload_to=upload_location, null=True)
    bio = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name

    @property
    def total_address(self):
        return f'{self.address} {self.zip_code}, {self.city}, {self.country}'
