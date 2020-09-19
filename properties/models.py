from django.db import models
from django.urls import reverse
import re

# Create your models here.
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError
from agents.models import Agent


def upload_location(instance,filename):
	  return "%s/%s" %(instance, filename)


def phone_validator(value):
    reg = re.compile(r'^\d\d\d\d\d\d\d\d\d\d$')
    number = reg.match(value)
    if number is None:
      raise ValidationError("The number is not valid")
    return value

choices = (('sell', 'sell'), ('rent', 'rent'))

class Property(models.Model):
    name = models.CharField(max_length=30)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True,null=True)
    type = models.CharField(max_length=20, choices=choices, default='sell')
    description = models.TextField(max_length=400,null=True)
    price = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=upload_location)
    view_count = models.IntegerField(default=0)
    sold = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Properties"

    def raise_view_count(self):
        self.view_count = self.view_count +1
        return True

    def get_absolute_url(self):
        return reverse("properties:individual_property", kwargs={"slug": self.slug})

    def __str__(self):
        return "%s" % self.name


class OrderProperty(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='orderuser', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, related_name='property', on_delete=models.CASCADE)
    message = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Ordered Properties"

    def total_price(self):
      marked_price = float(self.property.price)
      return marked_price

    def __str__(self):
        return self.property.name


class RentProperty(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='rent_user', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, related_name='rent_property', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    message = models.TextField(max_length=200, null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Rented Properties"

    def __str__(self):
        return self.property.name


class InspectProperty(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='inspect_user', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, related_name='inspect_property', on_delete=models.CASCADE)
    inspect_datetime = models.DateTimeField()
    message = models.TextField(max_length=200, null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Inspected Properties"

    def __str__(self):
        return self.property.name


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
      slug = new_slug
    qs = Property.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
      new_slug = "%s-%s" %(slug, qs.first().id)
      return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
      instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Property)
